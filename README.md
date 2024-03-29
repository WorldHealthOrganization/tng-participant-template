# Introduction

This repository contains the template for building [onboarding](https://github.com/WorldHealthOrganization/smart-trust/blob/main/input/pagecontent/concepts_onboarding.md) informations for the Smart Trust Network Attendees. This includes CSCAs, Auth information, signing information and other relevant files for onboarding a participant.

# Prerequisites

Collect this information and transfer it for each environment:

1) Create an private git repository on github.
2) Prepare the following information for onboarding request: 
    - Environment Repository (all private to hide uploader's identity) (DEV, UAT, PROD)
    - Repository URL
    - Invite WHO Bot User to Repository (with read rights). The Bot User is: [tng-bot](https://github.com/tng-bot) for production and [tng-bot-dev](https://github.com/tng-bot-dev) for development and acceptance environments.
    - Create GPG Keys for responsible persons for each environment (for tagging)
3) Fill in content for your country:
   - for DEV and UAT environments you may use the conf files and the [certgen bash script](scripts/certgen/gen_all_certs.sh) as a guideline

4) Send an onboarding/participation request to tng-support@who.int

# GPG Keys

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


# Domains

For further domains, add a new folder under onboarding and copy the DCC folder structure.

Available Domains:

- DCC
- DDCC
- DIVOC
- ICAO
- SHC
- CRED
- RACSEL-DDVC
- IPS

# Trusted Issuer

To onboard [Trusted Issuer](onboarding/DDCC/ISSUER/trusted-issuer-onboarding-specification.md), provide input via the subfolder ISSUER.

