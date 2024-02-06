from common import requires_readable_cert, warn_in_sync_mode

@warn_in_sync_mode
@requires_readable_cert
def test_key_usages(cert):
    """Check if the certificates have the required keyUsage flags 
       depending on certificate group and file name"""
    assert '2.5.29.15' in cert.extensions, 'keyUsage not in x509 extensions'
    usages = cert.extensions['2.5.29.15'].value

    # TLS client certs in TLS group
    if cert.pathinfo.get('group').upper() == 'TLS'\
    and cert.pathinfo.get('filename').startswith('TLS'):  
        assert usages.digital_signature == True, 'TLS cert should have usage flag "digital signature"'
        assert usages.crl_sign == False, 'TLS cert should not have usage flag "CRL sign"'
        # ... TODO
    # CA certs in TLS group
    elif cert.pathinfo.get('group').upper() == 'TLS'\
    and cert.pathinfo.get('filename').upper().startswith('CA'):  
        pass
    elif cert.pathinfo.get('group').upper() == 'UP':  
        assert usages.digital_signature == True, 'UP cert should have usage flag "digital signature"'
        assert usages.crl_sign == False, 'UP cert should not have usage flag "CRL sign"'
        # ... TODO
    elif cert.pathinfo.get('group').upper() == 'SCA':
        assert usages.key_cert_sign == True, 'SCA should have usage flag "key cert sign"'
