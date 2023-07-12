from common import requires_readable_cert
from cryptography import x509

@requires_readable_cert
def test_subject_format(cert, pytestconfig):
    country_attributes = cert.x509.subject.get_attributes_for_oid(x509.NameOID.COUNTRY_NAME)
    assert len(country_attributes) == 1, 'Certificate must have 1 C attribute'
    #common_name_attributes = cert.x509.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    #assert len(common_name_attributes) == 1, 'Certificate must have 1 CN attribute'