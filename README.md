# Introduction

This repository contains the template for building [onboarding](https://github.com/WorldHealthOrganization/smart-trust/blob/main/input/pagecontent/concepts_onboarding.md) informations for the Smart Trust Network Attendees. This includes CSCAs, Auth information, signing information and other relevant files for onboarding a participant.

# Prerequisites

Collect this information and transfer it for each environment:

1. Create an private git repository on github.
2. Prepare the following information for onboarding request: 
    1. Environment Repository (all private to hide uploader's identity) (DEV, UAT, PROD)
    2. Repository URL
    3. Invite WHO Bot User to Repository (with read rights). The Bot User is:
        - [tng-bot](https://github.com/tng-bot) for production (PROD)
        -  [tng-bot-dev](https://github.com/tng-bot-dev) for development (DEV) and user acceptance testing (UAT) environments.
    4. Create GPG Keys for responsible persons for each environment (see below)
3. Fill in content for your country:
   - for DEV and UAT environments you may use the conf files and the [certgen bash script](scripts/certgen/gen_all_certs.sh) as a guideline according to the [Certificate Preparation](scripts/certgen/README.md)

4. Send an onboarding/participation request to tng-support@who.int which contains:
   - URL of the private repository created in Step 1
   - The GPG key exported in Step 3.iv
   

# Creating GPG Keys

Follow the [instructions](https://docs.github.com/en/authentication/managing-commit-signature-verification/generating-a-new-gpg-key) to create a key.

Algorithm RSA or EC.
Minimum Keylength 4096 bit (RSA) or 256 bit (EC)

# Procedure

1) The Repo will be onboarded + the Public GPG keys. Export it by using: 
```
gpg --armor --export [key-id]
```
Keys can be listed by:
```
gpg -k
```
2) Tag the version of your latest informations by using [git tag + signing](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work) commands either from terminal or developer IDE. Please Note that an update in github web desktop itself is not working, because the platform will use an intermediate key.
3) The Bot user clones the latest tag of your private repo and verifies the signature of the tag against the onboarded GPG keys
4) After verification the content will be taken over for your country
5) The bot creates a PR


# Trust Domains

Supported Domains:

- DCC
- DDCC
- DIVOC
- ICAO
- SHC
- CRED
- RACSEL-DDVC
- IPS-PILGRIMAGE

## Adding a new trust domain

New trust domains can be established only in agreement between the requesting party and WHO.
Collaborate with the WHO's secretariat to gather comprehensive insights and feedback for the development of the new trust domain.

Once the new trust domain is established create new subdirectory in 'onboarding' subdir that reflect the agreed domain name.
If you are already onboarded for a domain (e.g. DCC, RACSEL-DDVC etc.) you only need to provide SCA for the the newly added domain.  This can either be an existing SCA or a new SCA.
If the newly added domain is the first one for this participant, UPLOAD, TLS and SCA must be generated.

# Trusted Issuer

To onboard [Trusted Issuer](onboarding/DDCC/ISSUER/trusted-issuer-onboarding-specification.md), provide input via the subfolder ISSUER.

