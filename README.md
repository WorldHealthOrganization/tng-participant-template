# Introduction

This repository contains the template for building [onboarding](https://smart.who.int/trust/concepts_onboarding.html) informations for the Smart Trust Network Attendees. This includes CSCAs, Auth information, signing information and other relevant files for onboarding a participant.

# Concepts Onboarding Checklist - Technical Procedure:

The [Concepts Onboarding Checklist](https://smart.who.int/trust/concepts_onboarding_checklist.html) on the Smart-Trust platform is specifically designed to be followed by countries or their representatives as part of the onboarding process. It includes all prerequisites, technical procedures, and necessary commands.

# Trust Domains

Supported Domains are listed in the [Trust Domain Code System](http://smart.who.int/trust/CodeSystem-WHO.TRUST.DOMAIN.html)

## Adding a new trust domain

New trust domains can be established only in agreement between the requesting party and WHO.
Collaborate with the WHO's secretariat to gather comprehensive insights and feedback for the development of the new trust domain.

Once the new trust domain is established create new subdirectory in 'onboarding' subdir that reflect the agreed domain name.
If you are already onboarded for a domain (e.g. DCC, IPS-PILGRIMAGE,DICVP,PH4H etc.) you only need to provide SCA for the the newly added domain.  This can either be an existing SCA or a new SCA.
If the newly added domain is the first one for this participant, UPLOAD, TLS and SCA must be generated.

# Trusted Issuer

To onboard [Trusted Issuer](onboarding/DDCC/ISSUER/trusted-issuer-onboarding-specification.md), provide input via the subfolder ISSUER.

