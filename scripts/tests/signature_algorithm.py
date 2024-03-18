from common import requires_readable_cert, warn_in_sync_mode
from cryptography.x509 import ObjectIdentifier as OID
from cryptography import x509

@requires_readable_cert
@warn_in_sync_mode
def test_signature_algorithm(cert):
    'Algorithm must be in allowed list'
    assert isinstance(cert.x509, x509.Certificate)
    allowed_OIDs = (OID('1.2.840.10045.4.3.2'), # ecdsa-with-SHA256
                    #OID('1.2.840.10045.4.3.3'), # ecdsa-with-SHA384
                    OID('1.2.840.113549.1.1.10'), # rsassa-pss
                    OID('2.16.840.1.101.3.4.3.2'), # dsaWithSha256
                    OID('1.2.840.113549.1.1.11'), # Legacy: sha256WithRSAEncryption
                    )
    
    assert cert.x509.signature_algorithm_oid in allowed_OIDs, f'Signature algorithm not allowed: {cert.x509.signature_algorithm_oid}'    
