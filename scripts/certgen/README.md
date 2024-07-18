# Certificate preparation

Following [Certificate Preperation](https://worldhealthorganization.github.io/smart-trust/concepts_CertificatePreperation.html) prepare conf files and execute cert generation script.

Disclaimer: The script generates self-signed certificates not intended to be used on production environments.

You must adapt the configuration file [template.cnf](template.cnf) to your needs:

Then execute the script. It will generate all certificates and keys in a subfolder named by current datetime.

```
cd scripts/certgen
./gen_all_certs.sh template.cnf
```

**Note: keep your private keys safe and secure. Do not share them with anyone.**
=======
## Execution On Windows
Windows plattform you can use [gen_all_certs.ps1](gen_all_certs.ps1) instead. 
Please note that you need to have [OpenSSL installed](https://slproweb.com/products/Win32OpenSSL.html) (e.g. Win64 OpenSSL v3.3.0 Light) and added to your PATH environment variable.
Also you may need allow the execution by setting an execution policy

```
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope Process
```

# Prepare Folders

Copy the generated certificates to the respective folders.  

# Tagging for taking into use

Finally commit push changes and make a signed tag for the version you want to take into use.

```
git add .
git commit -m "feat(cert): update certificates for onboarding"
git tag -s <YOUR-TAGNAME> -m 'onboardingRequest'
git push --tags
```

# Generate DSCs  
After onboarding you probably want to generate and upload your DSCs.
DSC Genration can be performed with the [gen_dsc.sh](gen_dsc.sh) script.
For execution replace \<SUBDIR\> with the path where your SCA.key and SCA.pem reside.
Optionally the purpose of the DSC can be provided with the third parameter. When this is omitted,
then the DSCs will be suitable for test, vaccination and recovery.
```
gen_dsc.sh template.cnf <SUBDIR> [test|vax|rec]
```
# Upload DSCs
For uploading DSCs they must be packend into an CMS and be signed with the Upload Certificate of their issuer.
The resulting output must be base64 encoded and put in the payload of a POST request to the TNG.
A script [upload_dsc.sh](upload_dsc.sh) performs these tasks and may be tailored to your needs.
