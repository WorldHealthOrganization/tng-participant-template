from common import collect_onboarding_files, PemFileWrapper
from common import load_multipart_pem_file, onboarding_folder_full_path
from common import _PATHINDEX
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.dsa import DSAPublicKey
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePublicKey, ECDSA
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes

def test_if_tls_resolves(country_folder):
    '''For every domain in the country_folder:
        - parse all x509 certs from all .pem files in the TLS subfolder
        - put all CA*.pem certs in a cert store
        - validate all TLS*.pem certs against that store

    '''
    ofiles = collect_onboarding_files(country_folder)

    for domain in ofiles:        
        certs = []        
        # Get all .pem files from the TLS subfolder
        tls_files = [ file for file in ofiles[domain] \
                        if len(file) >= 2 
                        and file[_PATHINDEX.GROUP].upper() == 'TLS' \
                        and file[_PATHINDEX.FILENAME].lower().endswith('.pem')]
        
        # Load and parse all x509 certs from these pem files
        print(f'INFO: {domain} {tls_files}')
        for tls_file_tuple in tls_files: 
            certs.extend(load_multipart_pem_file(
                onboarding_folder_full_path(country_folder, domain, tls_file_tuple)))
    
        # For all certs which's filename starts with 'TLS'
        for cert in filter(lambda cert: cert.pathinfo['filename'].upper().startswith('TLS'), certs):
            assert isinstance(cert, PemFileWrapper)
            verified = False
            # For all certs which's filename starts with 'CA':
            for ca_cert in filter(lambda cert: cert.pathinfo['filename'].upper().startswith('CA'), certs):
                assert isinstance(ca_cert, PemFileWrapper)
                try:
                    if isinstance(ca_cert.x509.public_key(), DSAPublicKey):
                        ca_cert.x509.public_key().verify(
                            cert.x509.signature,
                            cert.x509.tbs_certificate_bytes,
                            cert.x509.signature_hash_algorithm
                        )
                    elif isinstance(ca_cert.x509.public_key(), EllipticCurvePublicKey):
                        ca_cert.x509.public_key().verify(
                            cert.x509.signature,
                            cert.x509.tbs_certificate_bytes,
                            ECDSA(cert.x509.signature_hash_algorithm)
                        )
                    else:
                        ca_cert.x509.public_key().verify(
                            cert.x509.signature,
                            cert.x509.tbs_certificate_bytes,
                            padding.PKCS1v15(),
                            cert.x509.signature_hash_algorithm
                        )
                    verified = True
                    print(f'{cert.pathinfo["filename"]}:{cert.index} verified by {ca_cert.pathinfo["filename"]}:{ca_cert.index}')
                except InvalidSignature:
                    pass # This means we just have to keep looking
                except Exception:
                    raise # Something went wrong 
            if not verified:
                print(f'{cert.pathinfo["filename"]}:{cert.index} not verified by any CA')
            assert verified, f'Could not find a signing CA for {cert.pathinfo["filename"]}'