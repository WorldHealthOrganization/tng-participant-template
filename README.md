# Introduction

This repository contains the template for building onboarding informations for the Smart Trust Network Attendees. This includes CSCAs, Auth information, signing information and other relevant files for onboarding a participant.

# Prerequisites

1) Create an private git repository either on github, gitlab or similiar. 
2) Prepare the following information for onboarding request: 
    - Environment (DEV, UAT, PROD)
    - Repository URL
    - (Optional) Access Token for Repository
    - GPG Keys of responsible persons

# Procedure

1) Fork/Clone this repository for Dev, UAT and Prod in your github repository. Ensure that at least the prod repository is private to disclose the identity of the uploaders. 
2) Add to this repositories the Bot User XXXXXXXXX
3) Prepare for each environment GPG Key Pairs
4) Create Tags for new Informations and sign it with the GPG Pairs
