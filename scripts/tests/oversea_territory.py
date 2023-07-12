from common import requires_readable_cert
import pytest
from cryptography import x509

@requires_readable_cert
def test_oversea_territory_ou(cert):
    pytest.skip(reason='Not implemented yet') # TODO: implement for ICAO

    state_prov_attr = cert.x509.subject.get_attributes_for_oid(x509.NameOID.STATE_OR_PROVINCE_NAME)
    ju_country_attr = cert.x509.subject.get_attributes_for_oid(x509.NameOID.JURISDICTION_COUNTRY_NAME)