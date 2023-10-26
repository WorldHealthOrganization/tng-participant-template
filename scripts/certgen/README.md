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
After onboarding you probably want to upload your DSCs.
DSC Genration can be performed with the [gen_dsc.sh](gen_dsc.sh) script.
For execution replace \<SUBDIR\> with the path where your SCA.key and SCA.pem reside.
```
gen_dsc.sh template.cnf <SUBDIR>
```
