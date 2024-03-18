from datetime import datetime, timedelta
from common import requires_readable_cert, warn_in_sync_mode

@requires_readable_cert
@warn_in_sync_mode
def test_validity(cert):
    '''Onboarded certificates must be valid for at least 30 days from now'''
    assert cert.x509.not_valid_after >= datetime.now()+timedelta(days=30),\
        "Certificate expires in less than 30 days"