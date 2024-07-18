from common import collect_onboarding_files

def test_folder_mandatory_files(country_folder):
    'Check if mandatory files exist in folder'

    ofiles = collect_onboarding_files(country_folder)

    assert len(ofiles) >= 1, 'There must be at least one domain'

    # Initialize flags for each certificate
    tls_cert_found = False
    tls_ca_cert_found = False
    up_cert_found = False

    # Testing folder structure
    for domain in ofiles.keys():
        assert domain in ('DCC','DDCC','DIVOC','ICAO','SHC','CRED','RACSEL-DDVC','IPS-PILGRIMAGE'), 'Invalid domain: '+domain

        # Check if certificates are present in the current domain
        if ('TLS', 'TLS.pem') in ofiles[domain]:
            tls_cert_found = True
        if ('TLS', 'CA.pem') in ofiles[domain]:
            tls_ca_cert_found = True
        if ('UP', 'UP.pem') in ofiles[domain]:
            up_cert_found = True

        # Assert if 'SCA' folder and 'SCA.pem' file are missing in the current domain
        assert ('SCA', 'SCA.pem') in ofiles[domain], f'SCA folder or SCA.pem file is missing in domain {domain}'

    # Assert that each certificate was found in at least one domain
    assert tls_cert_found, 'TLS cert is missing in all domains'
    assert tls_ca_cert_found, 'TLS/CA cert is missing in all domains'
    assert up_cert_found, 'UP cert is missing in all domains'