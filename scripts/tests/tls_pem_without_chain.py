from common import collect_onboarding_files, onboarding_folder_full_path

def test_tls_pem_without_chain(country_folder): 
    'Checks if a TLS cert comes without a chain'

    ofiles = collect_onboarding_files(country_folder)
    print(ofiles)

    for domain in ofiles.keys():        
        tls_files = [ file for file in ofiles[domain] \
                        if len(file) >= 2 
                        and file[-2].upper() == 'TLS'\
                        and file[-1].upper().startswith('TLS') ]

        print(tls_files)
        for tls_file_tuple in tls_files:
            full_file_name = onboarding_folder_full_path(country_folder, domain, tls_file_tuple)

            with open(full_file_name) as tls_file: 
                count_begin = 0
                for line in tls_file: 
                    if '-----BEGIN' in line:
                        count_begin += 1
                assert count_begin == 1, f'{full_file_name} must contain EXACTLY ONE certificate'
