from common import requires_readable_cert, warn_in_sync_mode
import pytest
from cryptography import x509

@requires_readable_cert
@warn_in_sync_mode
def test_extended_key_usages(cert):
    """Extended key usage for TLS and UP certs must be set"""
    if cert.pathinfo.get('group').upper() == 'SCA'\
    or cert.pathinfo.get('group').upper() == 'UP'\
    or cert.pathinfo.get('group').upper() == 'TLS' and cert.pathinfo.get('filename').upper().startswith('CA'):
        #pytest.skip(reason='CA/SCA or UP certs do not require extended key usage')
        return # Pass: CA/SCA or UP certs do not require extended key usage


    assert '2.5.29.37' in cert.extensions, 'extendedKeyUsage not in extensions'
    usages = cert.extensions['2.5.29.37'].value._usages
    
    if cert.pathinfo.get('group').upper() == 'TLS'\
    and cert.pathinfo.get('filename').upper().startswith('TLS'):
        assert x509.ObjectIdentifier('1.3.6.1.5.5.7.3.2') in usages, 'TLS (AUTH) certificates must allow clientAuthentication'
