from common import requires_readable_cert

@requires_readable_cert
def test_basic_constraints(cert):
    '''Only CA and SCA certs may have a CA:TRUE constraint'''

    assert '2.5.29.19' in cert.extensions, 'basicConstraints not in x509 extensions'
    basicConstraints = cert.extensions['2.5.29.19'].value

    if cert.pathinfo.get('group').upper() == 'SCA'\
    or cert.pathinfo.get('group').upper() == 'TLS' and cert.pathinfo.get('filename').upper().startswith('CA'):
        assert basicConstraints.ca == True, 'SCA and CA certs must have basicConstraints(CA:TRUE)'
        assert not basicConstraints.path_length, 'Path length must be 0 or None'
    else:
        assert not basicConstraints.ca == True, 'non-CA certs must NOT have basicConstraints(CA:TRUE)'