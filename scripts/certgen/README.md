# Certificate preparation

Following [Certificate Preperation](https://worldhealthorganization.github.io/smart-trust/concepts_CertificatePreperation.html) prepare conf files and execute cert generation script.

Disclaimer: The script generates self-signed certificates not intended to be used on production environments.

You must adapt the following default certificate parameter in [gen_all_certs.sh](gen_all_certs.sh) to your needs:

```
export OSSL_COUNTRY_NAME="XA"
export OSSL_STATE_NAME="Test State"
export OSSL_LOCALITY_NAME="Geneva"
export OSSL_ORGANIZATION_NAME="WHO"
export OSSL_ORGANIZATIONAL_UNIT_NAME="R&D"
```

Then execute the script. It will generate all certificates and keys in a subfolder named by current datetime.

```
cd scripts/certgen
./gen_all_certs.sh
```

## Execution On Windows
Windows plattform you can use [gen_all_certs.ps1](gen_all_certs.ps1) instead. 
Please note that you need to have [OpenSSL installed](https://slproweb.com/products/Win32OpenSSL.html) (e.g. Win64 OpenSSL v3.3.0 Light) and added to your PATH environment variable.
Also you may need allow the execution by setting an execution policy

```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```

# Prepare Folders

Note: keep your private keys safe and secure. Do not share them with anyone. 

Copy the generated certificates to the respective folders and change the file names to match the naming convention.
For the case of self-signed TLS certificates, the CA.pem is just a copy of the TLS.pem (check to have keyCertSign in the keyUsage).
The CA.pem should exist, since it is used to verify the TLS client certificate when connecting to the TNG application.

# Tagging for taking into use

Finally commit push changes and make a signed tag for the version you want to take into use.

```
git add .
git commit -m "feat(cert): update certificates for onboarding"
GIT_TRACE=1 git tag -s v0.0.1 -m 'onboardingRequest'
git push --tags
```
