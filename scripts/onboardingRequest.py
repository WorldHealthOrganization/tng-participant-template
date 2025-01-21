import os
import sys
import operator

def collect_onboarding_files(country_folder, convert_upper=False):
    '''  Create a dict of tuples for all found files:
         The key is the domain (DCC, ICAO, etc.)
         Each tuple contains the path starting from the domain folder,
            e.g. ('TLS','TLS.pem')
    '''
    offset = len(country_folder.split(os.sep))
    onboardings = {}
    for path, dirs, files in os.walk(country_folder):
        for file in files:
            fpath = os.path.join(path, file)
            if convert_upper:
                fpath = fpath.upper()
            long_path = tuple(fpath.split(os.sep)[offset:])
            # If we're not scanning country folders but directly an onboarding folder
            if country_folder==f'.{os.sep}onboarding':
                long_path = ('onboarding',)+long_path

            # Ignore other folders than 'onboarding'
            if long_path[0].lower() == 'onboarding':
                domain = long_path[1]
                if domain.startswith('.'):
                    continue # Allow folders like .git, files like .gitignore, etc. to be
                    # present without being seen as onboarding files
                if not domain in onboardings:
                    onboardings[domain] = []
                onboardings[domain].append(long_path[2:])
    return onboardings

repo = sys.argv[1]

if repo == "repo":
  with open('temp/verifyResult') as f:
    result = f.readline()   
    if not result:
        raise Exception("Bad verification.")
    else:
        os.system("echo 'Verification was good.'")

with open('temp/country') as f:
  country = f.readline().replace("\n","")

branchName = country + "/onboardingRequest"

os.system("git checkout -b" + branchName +" > /dev/null 2>&1")
os.system("rm -rf "+country)
os.system("mkdir -p " + country)
os.system("mkdir -p " + country+"/onboarding")

# Retrieve environment variable and convert to tuple
allowed_domains = tuple(os.environ.get("ALLOWED_DOMAINS", "").split(", "))
print(f'Length of allowed domains is: {len(allowed_domains)}', flush=True)
print(f'Allowed domains is: {allowed_domains}', flush=True)

#os.system("cp -r "+repo+"/onboarding " + country )

source_path = os.path.join(repo, 'onboarding')
destination_path = country
os.system(f"cp -r {source_path} {destination_path}")

ofiles = collect_onboarding_files(destination_path)
country_domains = ofiles.keys()

for domain in list(country_domains):
    if operator.countOf(allowed_domains, domain) == 0: # if domain not in allowed_domains
        os.system("rm -rf "+destination_path+"/onboarding/"+domain)

os.system("[ -e "+country+"/onboarding/DCC/TLS/Report ] && cat "+country+"/onboarding/DCC/TLS/Report")
os.system("[ -e "+country+"/onboarding/DCC/TLS/Report ] && rm "+country+"/onboarding/DCC/TLS/Report")

if os.path.exists("sync"):
  if os.path.exists(country+"/onboarding/DCC/UP/UP_SYNC.pem"):
      os.system("rm "+country+"/onboarding/DCC/UP/UP_SYNC.csr")
else:
    if os.path.exists(country+"/onboarding/DCC/UP/UP_SYNC.pem"):
      os.system("rm "+country+"/onboarding/DCC/UP/UP_SYNC.pem")

os.system("[ -d "+country + "/onboarding/DCC/auth"+" ] && mv " + country + "/onboarding/DCC/auth "+ country+"/onboarding/DCC/TLS")
os.system("[ -d "+country + "/onboarding/DCC/csca"+" ] && mv " + country + "/onboarding/DCC/csca "+ country+"/onboarding/DCC/SCA")
os.system("[ -d "+country + "/onboarding/DCC/up"+" ] && mv " + country + "/onboarding/DCC/up "+ country+"/onboarding/DCC/UP")
os.system("[ -f "+country + "/onboarding/DCC/SCA/CSCA.pem"+" ] && mv " + country + "/onboarding/DCC/SCA/CSCA.pem "+ country+"/onboarding/DCC/SCA/SCA.pem")

#if not os.path.exists("TT_API_ACCESS"):
      #os.system("rm -rf "+country+"/onboarding/DCC/TLS")

##### Try to sign it

if os.environ.get("ENV") != "PROD":
    os.system("echo Start signing for " + country)
    os.system("./scripts/signing/sign-json.sh ./sign " +country)
    os.system("./scripts/signing/add_signature_to_trusted_issuer_json.sh  sign/cas/TA/certs/TNG_TA.pem sign/cas/TA/private/TNG_TA.key.pem " + country)
else:
     os.system("echo No secret for TA found. Skip signing.")

####################

os.system("git add "+ country + " > /dev/null 2>&1")

result = os.popen("git commit -m 'Bot added Files from "+country+"'").read()

if not "nothing added to commit" in result:
  os.system("git push -f -u origin "+ branchName +" > /dev/null 2>&1")


#> /dev/null 2>&1
os.system("tree")
