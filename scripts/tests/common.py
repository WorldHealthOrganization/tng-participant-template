import functools
import pytest
import os 
from cryptography import x509
from base64 import urlsafe_b64decode
import json
from warnings import warn

def requires_readable_cert(func):
    'Decorator for tests that should be skipped if the cert has not been loaded'
    @functools.wraps(func)
    def wrapper(cert, *args, **kwargs):
        if not cert or cert.error: 
            pytest.skip(reason='Certificate could not be loaded')
        else: 
            return func(cert,*args, **kwargs)
    return wrapper

def warn_in_sync_mode(func):
    '''Decorator for tests that should only yield a warning in sync mode
      (only works for tests that have a cert parameter)'''
    @functools.wraps(func)
    def wrapper(cert, *args, **kwargs):
        # Step 1: Get SECRETS variable as JSON
        try:
            secrets = json.loads(os.environ.get('SECRETS'), strict=False)
        except: # Assume secrets is empty if it cannot be loaded
            secrets = {}


        # Step 2: Check if country of cert has a sync flag that is True
        country = cert.pathinfo.get('country')
        if country in secrets \
            and _padded_b64_json(secrets.get(country)).get('sync'):
                sync_flag = True
        else:
                sync_flag = False

        # Step 3: Run the test and catch any exception
        #         if no exception is raised, the test is passed
        try:
            return func(cert,*args, **kwargs)
        # Step 4: Test is failed
        #         If sync_flag is True, just raise a warning
        #         else raise the original exception
        except AssertionError as ae:
            if sync_flag:
                warn(" ".join(ae.args),stacklevel=2)
            else:
                raise ae
        except Exception as e:
            if sync_flag:
                warn(f"{e}", source=e)
            else:
                raise e
    return wrapper



@functools.lru_cache(maxsize=64)
def _padded_b64_json(envvalue):
    '''Corrects the padding of a b64_url encoded string and
        then decodes it. Returns empty dict on error.
    '''
    try:
        while len(envvalue) % 4 != 0:
            envvalue += '='
        return json.loads(urlsafe_b64decode(envvalue),strict=False)
    except:
        return {}

@functools.lru_cache(maxsize=128)
def collect_onboarding_files(country_folder, convert_upper=False):
    '''  Create a dict of tuples for all found files:
         The key is the domain (DCC, ICAO, etc.)
         Each tuple contains the path starting from the domain folder, 
            e.g. ('TLS','TLS.pem')
    '''
    offset = len(country_folder.split(os.sep))
    onboardings = {}
    for path, dirs, files in os.walk(country_folder):
        for file in files: 
            fpath = os.path.join(path, file)
            if convert_upper:
                fpath = fpath.upper()
            long_path = tuple(fpath.split(os.sep)[offset:])
            # If we're not scanning country folders but directly an onboarding folder
            if country_folder==f'.{os.sep}onboarding':
                long_path = ('onboarding',)+long_path

            # Ignore other folders than 'onboarding'
            if long_path[0].lower() == 'onboarding':
                domain = long_path[1]
                if domain.startswith('.'):
                    continue # Allow folders like .git, files like .gitignore, etc. to be
                             # present without being seen as onboarding files
                if not domain in onboardings:
                    onboardings[domain] = []
                onboardings[domain].append(long_path[2:])
    return onboardings

def onboarding_folder_full_path(country_folder, domain, path_tuple):
    '''Depending on whether one is in country mode or not, the 
       country folder may contain the 'onboarding' folder itself 
       or not. 
       This function attempts to distinguish the two cases and to
       return the full path of a tuple returned by `collect_onboarding_files`
       with its domain.
    '''

    if not 'onboarding' in country_folder:
        country_folder = os.path.join(country_folder, 'onboarding')
    return os.path.join(country_folder, domain,  *path_tuple)

class _PATHINDEX:
    FILENAME = -1
    GROUP = -2
    DOMAIN = -3
    COUNTRY = -5    

def load_multipart_pem_file(pem_file_path):
    '''Return a tuple of PemFileWrapper instances for each certificate
    in the pem file. The index attribute of the PemFileWrapper indicates
    which certifiate inside the file it represents.'''
    data = []
    with open(pem_file_path) as pem_file: 
        for line in pem_file:
            if '-----BEGIN CERTIFICATE-----' in line:
                data.append((bytes(line,'utf-8'))) # initialize buffer
            elif len(data)>0:
                data[-1]+=bytes(line,'utf-8')
    
    wrappers = []
    for index, _data in enumerate(data):
        wrappers.append(PemFileWrapper(pem_file_path, _data))
        wrappers[-1].index = index
    
    return tuple(wrappers)

class PemFileWrapper:
    file_name = None
    error = None
    pathinfo = {}
    extensions = {}
    index = 0 # If multiple certificates are in one pem file
    
    def __init__(self, pem_file, override_bytes=None):
        self.file_name = os.path.normpath(pem_file)
        try: 
            if override_bytes: 
                source = override_bytes
            else: 
                source = open(self.file_name,'rb').read() 

            self.x509 = x509.load_pem_x509_certificate(source)
            self.extensions = {}
            for ex in self.x509.extensions:
                self.extensions[ ex.oid.dotted_string ] = ex 
                if not ex.oid._name == 'Unknown OID':
                    self.extensions[ ex.oid._name ] = ex
        except Exception as ex: 
            self.error = ex
            self.x509 = None

        try: 
            self.pathinfo = {}
            path = self.file_name.split(os.sep)
            self.pathinfo['filename'] = path[_PATHINDEX.FILENAME] # CA.pem, TLS.pem, UP.pem ...
            self.pathinfo['group'] = path[_PATHINDEX.GROUP] # up, csca, auth
            self.pathinfo['domain'] = path[_PATHINDEX.DOMAIN] # DCC, DIVOC, SHC
            # This last one may fail when there is no country info in the path
            self.pathinfo['country'] = path[_PATHINDEX.COUNTRY] # GER, BEL, FIN ...
        except:
            pass

