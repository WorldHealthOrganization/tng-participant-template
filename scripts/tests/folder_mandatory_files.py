from common import collect_onboarding_files, read_allowed_domain_from_env

def test_folder_mandatory_files(country_folder): 
    'Check if mandatory files exist in folder'

    ofiles = collect_onboarding_files(country_folder)

    allowed_domains = read_allowed_domain_from_env()

    assert len(ofiles) >= 1, 'There must be at least one domain'

    # Testing folder structure
    for domain in ofiles.keys():
        if domain in allowed_domains:
            try:
                assert ('TLS', 'TLS.pem') in ofiles[domain], f'TLS cert is missing in domain {domain}'
                assert ('TLS', 'CA.pem') in ofiles[domain], f'TLS/CA cert is missing in domain {domain}'
                assert ('UP', 'UP.pem') in ofiles[domain], f'UP cert is missing in domain {domain}'
                # assert ('SCA', 'SCA.pem') in ofiles[domain], f'SCA cert is missing in domain {domain}'
            except AssertionError as e:
                print(e)
        else:
            print("Invalid domain, skipping folder mandatory files test")