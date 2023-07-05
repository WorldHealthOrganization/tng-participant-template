import pycountry
import pytest
from common import requires_readable_cert
from cryptography import x509

@requires_readable_cert
def test_country_flag(cert, pytestconfig):
    'The country flag (C value) must be set to the correct country code'

    if not pytestconfig.getoption('country_mode'): 
        pytest.skip(reason='This test only runs in country mode')

    country_attributes = cert.x509.subject.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)
    
    if not country_attributes:
        # Check 1: Country attribute must be present
        assert False, 'No country attribute found'
    else:
        # Check 2: Country must be in the list of existing countries
        country = pycountry.countries.lookup(country_attributes[0].value)

    # Check 3: Country in path must match country of C attribute
    assert cert.pathinfo.get('country') == country.alpha_3