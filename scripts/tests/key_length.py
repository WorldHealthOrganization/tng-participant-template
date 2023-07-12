from common import requires_readable_cert
from cryptography.hazmat.primitives.asymmetric import ec, rsa, dsa


@requires_readable_cert
def test_key_length(cert):
    'The key length should be for RSA-PSS and DSS minimum 3072, and for EC-DSA 256 bit'

    public_key = cert.x509.public_key()

    if isinstance(public_key, rsa.RSAPublicKey):
        assert public_key.key_size >= 3072, f'RSA Key not long enough: {public_key.key_size}'
    elif isinstance(public_key, ec.EllipticCurvePublicKey):
        assert public_key.curve.key_size >= 256, f'EC Key not long enough: {public_key.curve.key_size}'
    elif isinstance(public_key, dsa.DSAPublicKey):
        assert public_key.key_size >= 3072, f'DSA Key not long enough: {public_key.key_size}'
    else:
        assert False, 'Unsupported key type'
