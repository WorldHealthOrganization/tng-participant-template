
def test_valid_group(cert):
    'The group in the path name must be valid'
    group = cert.pathinfo.get('group')
    assert group, 'Certificate at incorrect location'
    assert group.upper() in ('UP', 'SCA', 'TLS'), 'Invalid group: ' + group

def test_valid_domain(cert):
    'The domain in the path name must be valid'

    domain = cert.pathinfo.get('domain')
    assert domain, 'Certificate at incorrect location'
    assert domain.upper() in ('DCC','DDCC','DIVOC','ICAO','SHC','CRED','RACSEL-DDVC','IPS-PILGRIMAGE'), 'Invalid domain: ' + domain