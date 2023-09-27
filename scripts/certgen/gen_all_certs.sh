#!/bin/zsh
# valid for 4 years
DAYS_CA=1461
# valid for 1 year
DAYS_TLS=365
# valid for 1 year
DAYS_UPLOAD=365

# configure the DN
export OSSL_COUNTRY_NAME="XA"
export OSSL_STATE_NAME="Test State"
export OSSL_LOCALITY_NAME="Geneva"
export OSSL_ORGANIZATION_NAME="WHO"
export OSSL_ORGANIZATIONAL_UNIT_NAME="R&D"
#export OSSL_COMMON_NAME="WHO International" # default entry of the corresponding config file will be used

# generate a new directory for each run
subdir=$(date +%Y%m%d%H%M%S)
mkdir -p ${subdir}
# generate the certificates and keys for the CA, TLS, and upload
openssl req -x509 -new -days ${DAYS_CA} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/CAprivkey.key -nodes -out ${subdir}/CAcert.pem -config sca.conf
openssl req -x509 -new -days ${DAYS_TLS} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/TNP_TLS.key -nodes -out ${subdir}/TNP_TLS.pem -config TLSClient.conf
openssl req -x509 -new -days ${DAYS_UPLOAD} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/TNP_UP.key -nodes -out ${subdir}/TNP_UP.pem -config uploadCert.conf
