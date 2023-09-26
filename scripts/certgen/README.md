# Certificate preparation

Following [Certificate Preperation](https://worldhealthorganization.github.io/smart-trust/concepts_CertificatePreperation.html) prepare conf files and execute cert generation script.

Disclaimer: The script generates self-signed certificates and is not intended to be used for production environments.

You may use environment variables to set the certificate parameters (see gen_all_certs script for details).

```
cd scripts/certgen
./gen_all_certs.sh
```

Note: keep your private keys safe and secure. Do not share them with anyone. 
The generated keys are created in a folder with current datetime as name to mitigate overwriting them.

Copy the generated certificates to the respective folders and change the file names to match the naming convention.
If using self-signed TLS certificates, you may copy it also as CA.pem (check to have keyCertSign in the keyUsage).
The CA.pem should exist, since it is used to verify the TLS client certificate when connecting to the TNG application.

# Tagging for taking into use

Finally commit push changes and make a signed tag for the version you want to take into use.

```
git add .
git commit -m "feat(cert): update certificates for onboarding"
GIT_TRACE=1 git tag -s v0.0.1 -m 'onboardingRequest'
git push --tags
```


