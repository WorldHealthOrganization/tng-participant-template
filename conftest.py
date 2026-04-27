import os
import json
import pytest
import warnings
import pycountry
from glob import glob
from functools import lru_cache
from scripts.tests.common import PemFileWrapper, _PATHINDEX

def pytest_addoption(parser):
    parser.addoption("--country-mode", action="store_true", help="Expect country folders")
    parser.addoption("-G", "--group", default=None, help="Filter group (TLS,UP,SCA)")
    parser.addoption("-C", "--country", default=None, help="Filter by country")
    parser.addoption("-D", "--domain", default=None, help="Filter domain (DCC,DDCC,ICAO,...)")



def _add_country(db, **params):
    '''Add a country to a pycountry database for the duration of this session.
       This is useful to patch testing countries into a list of countries.'''
    if not db._is_loaded:
        db._load()
    # Create an instance of the virtual country
    obj = db.data_class(**params)
    # Add it to the database
    db.objects.append(obj)
    # Update the indices
    for key, value in params.items():
        value = value.lower()
        if key in db.no_index:
            continue
        index = db.indices.setdefault(key, {})
        index[value] = obj

try:
    test_countries = json.load(open(os.path.join('scripts','tests','testing_countries.json')))
    for country_def in test_countries.get('countries'):
        _add_country(pycountry.countries, **country_def)
except Exception as ex:
    message = f"Testing countries could not be loaded ({str(ex)})"
    warnings.warn(message)


@lru_cache(maxsize=16)
def _glob_files(country_mode=False, base_dir='.' ):
    if country_mode: 
        country_dirs = glob(os.path.join(base_dir,'???')) 
    else:
        country_dirs = [os.path.join(base_dir,'onboarding')]        

    found_files = []
    for country_dir in country_dirs:
        for root, dirs, files in os.walk(country_dir):
            for file in files: 
                name, ext = os.path.splitext(file)
                if ext.lower() in ['.pem', '.crt']:
                    found_files.append(os.path.join(root, file))

    return found_files, country_dirs

def pytest_generate_tests(metafunc):
    ''' Walk all subfolders of the current directory that consist of 3 characters
        XOR walk the directory that has been specified in the --country-code parameter
        of the test run. 
        
        Generate a test execution matrix
            - All test cases that have a "pem_file" parameter
            - All pem files discovered in the directory walk
    ''' 

    def filter_by(pem_files, filter_value, filter_index):
       if not filter_value:
           return pem_files
       return [p for p in pem_files if p.split(os.sep)[filter_index].upper()\
                                         == filter_value.upper() ]
    
    config = metafunc.config
    pem_files, country_folders = _glob_files( config.getoption('country_mode') )
    if config.getoption('country') and not config.getoption('country_mode'):
        raise ValueError('Country filter cannot be applied if not running in country-mode.'+
                         ' Use --country-mode to enable this mode.')

    _country = config.getoption('country')
    # Accept branch names as country
    if _country and '/' in _country:
        _country = _country.split('/')[0]

    pem_files = filter_by(pem_files, config.getoption('group'), _PATHINDEX.GROUP )
    pem_files = filter_by(pem_files, _country, _PATHINDEX.COUNTRY )
    pem_files = filter_by(pem_files, config.getoption('domain'), _PATHINDEX.DOMAIN )

    country_folders = filter_by(country_folders, _country , 1 )

    # Parametrize all tests that have a "cert" parameter with the found cert files
    if "cert" in metafunc.fixturenames:
        metafunc.parametrize("cert", pem_files, indirect=True)

    # Parametrize all tests that have a "country" parameter with the found dirs
    if "country_folder" in metafunc.fixturenames:
        metafunc.parametrize("country_folder", country_folders, indirect=True)

_cert_cache = {}
@pytest.fixture
def cert(request):
    "the pem file that should be tested"
    if not request.param in _cert_cache:
        _cert_cache[request.param] = PemFileWrapper(request.param)
    return _cert_cache[request.param]

@pytest.fixture
def country_folder(request):
    return request.param


