from datetime import timedelta
from common import requires_readable_cert, warn_in_sync_mode

@requires_readable_cert
@warn_in_sync_mode
def test_validity_range(cert):
    '''SCA must be valid for at least 2 years and at most 4 years,
       UP, TLS must be valid for at least 1 year and at most 2 years
    '''
    validity = cert.x509.not_valid_after - cert.x509.not_valid_before
    
    if cert.pathinfo.get('group').upper() == 'SCA':
        min_years, max_years = 2, 4
    elif cert.pathinfo.get('group').upper() == 'TLS' \
        and cert.pathinfo.get('filename').upper().startswith('CA'):         
        return None # 'CA chain of TLS certs has no validity range restrictions'
    else: 
        min_years, max_years = 1, 2

    assert  validity > timedelta(days=min_years*365-1), \
       f"{cert.pathinfo.get('group')} must be valid for at least {min_years} years (is: {validity.days} days)"
    assert validity < timedelta(days=max_years*366), \
       f"{cert.pathinfo.get('group')} must be valid for at most {max_years} years (is: {validity.days} days)"

