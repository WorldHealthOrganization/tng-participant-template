import pycountry
import pytest
from common import requires_readable_cert
from cryptography import x509


def add_country(db, **params):
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


@requires_readable_cert
def test_country_flag(cert, pytestconfig):
    'The country flag (C value) must be set to the correct country code'

    add_country(pycountry.countries, alpha_2='XA', alpha_3='XXA', common_name='Test XA',
                                         flag='😄', name='Test XA', numeric='23233', official_name='Test Country XA' )
    add_country(pycountry.countries, alpha_2='XB', alpha_3='XXB', common_name='Test XA',
                                     flag='😄', name='Test XXB', numeric='2929', official_name='Test Country XB' )
    add_country(pycountry.countries, alpha_2='XY', alpha_3='XXY', common_name='Test XY',
                                     flag='😄', name='Test XY', numeric='9989', official_name='Test Country XY' )
    add_country(pycountry.countries, alpha_2='XX', alpha_3='XXX', common_name='Test XA',
                                     flag='😄', name='Test XX', numeric='9990', official_name='Test Country XX' )
    add_country(pycountry.countries, alpha_2='XL', alpha_3='XCL', common_name='Test LAC (XL, XCL)',
                                     flag='😄', name='Test XL', numeric='9991', official_name='Test Country XL' )
    add_country(pycountry.countries, alpha_2='XO', alpha_3='XXO', common_name='Test XO',
                                     flag='😄', name='Test XO', numeric='9992', official_name='Test Country XO' )
    countries = list(pycountry.countries)

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
    assert cert.pathinfo.get('country') == country.alpha_3, f"{cert.pathinfo.get('country')} != {country.alpha_3}"