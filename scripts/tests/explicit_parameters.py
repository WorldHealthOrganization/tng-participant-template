from common import requires_readable_cert
import pytest

@requires_readable_cert
def test_explicit_parameter(cert):
    pytest.skip(reason='Not implemented yet') # TODO: implement for ICAO
    