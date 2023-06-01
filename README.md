# Introduction

This repository contains the template for building onboarding informations for the Smart Trust Network Attendees. This includes CSCAs, Auth information, signing information and other relevant files for onboarding a participant.

# Prerequisites

1) Create an private git repository on github.
2) Prepare the following information for onboarding request: 
    - Environment Repository (all private to hide uploaders identity) (DEV, UAT, PROD)
    - Repository URL
    - Invite WHO Bot User to Repository (with read rights).
    - Create GPG Keys for responsible persons for each Environment (for tagging)
3) Fill in content for your country
# Procedure

1) The Repo will be onboarded + the GPG keys
2) The Bot user clones the latest tag of your private repo and verifies the signature of the tag against the onboarded GPG keys
3) After verification the content will be took over for your country
4) The bot creates a PR


# Domains

For further domains, add a new folder under onboarding and copy the DCC folder structure.

Available Domains: 

- DCC
- DDCC
- DIVOC
- ICAO
