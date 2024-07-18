from common import requires_readable_cert, warn_in_sync_mode
import pytest

@requires_readable_cert
@warn_in_sync_mode
def test_explicit_parameter(cert):
    pytest.skip(reason='Not implemented yet') # TODO: implement for ICAO
    