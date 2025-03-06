#!/bin/bash
# this script uploads the DSC to the TNG DEV
# a given subdir containing the DSC.pem and DSC.key is expected
# optionally, a domain can be passed as second parameter
# -----------------------------------------------------------------

if [ $# -lt 2 ]; then
    echo "Usage: $0 <subdir> (where <subdir> must contain UP.pem and UP.key) <DSC DIR> [Domain]"
    exit 1
fi
if ! [ -d "$2" ]; then
    echo "No DSC DIR specified, second parameter must be a directory"
    exit 1
fi
if [ -z $3 ]; then
    echo "No domain specified: using DCC" #TODO: change to DDCC when accepted by TNG
    domain=DCC
else
    domain=$3
fi

subdir=$1
dsc_dir=$2

openssl x509 -outform der -in ${dsc_dir}/DSC.pem -out ${dsc_dir}/DSC.der
openssl cms -sign -nodetach -in ${dsc_dir}/DSC.der -signer ${subdir}/UP.pem -inkey ${subdir}/UP.key -out ${dsc_dir}/DSC_cms.der -outform DER -binary
openssl enc -base64 -in ${dsc_dir}/DSC_cms.der -e -A > ${dsc_dir}/DSC_cms.b64
#openssl x509 -in ${subdir}/DSC.pem -noout -fingerprint -sha256 | sed 's/://g' 
payload=$(cat ${dsc_dir}/DSC_cms.b64)

curl --location 'https://tng-dev.who.int/signerCertificate' \
--header 'Content-Type: application/cms' \
--key ${subdir}/TLS.key \
--cert ${subdir}/TLS.pem \
--data @${dsc_dir}/DSC_cms.b64

#cleanup
rm ${dsc_dir}/DSC.der
rm ${dsc_dir}/DSC_cms.der
rm ${dsc_dir}/DSC_cms.b64

