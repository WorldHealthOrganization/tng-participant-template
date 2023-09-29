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
# generate the certificates and keys for the SCA, TLS, and upload
openssl req -x509 -new -days ${DAYS_CA} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/SCA.key -nodes -out ${subdir}/SCA.pem -config sca.conf
openssl req -x509 -new -days ${DAYS_TLS} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/TLS.key -nodes -out ${subdir}/TLS.pem -config TLSClient.conf
openssl req -x509 -new -days ${DAYS_UPLOAD} -newkey ec:<(openssl ecparam -name prime256v1) -extensions ext -keyout ${subdir}/UP.key -nodes -out ${subdir}/UP.pem -config uploadCert.conf
#special case to only place CA.pem file for self-signed TLS cert as a copy
cat ${subdir}/TLS.pem > ${subdir}/CA.pem
