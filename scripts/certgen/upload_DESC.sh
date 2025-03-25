#!/bin/bash
# this script uploads the DESC to the TNG DEV
# a given subdir containing the DESC.pem and DESC.key is expected
# optionally, a domain can be passed as second parameter
# -----------------------------------------------------------------

if [ $# -lt 2 ]; then
    echo "Usage: $0 <subdir> (where <subdir> must contain UP.pem and UP.key) <DESC DIR> [Domain]"
    exit 1
fi
if ! [ -d "$2" ]; then
    echo "No DESC DIR specified, second parameter must be a directory"
    exit 1
fi
if [ -z $3 ]; then
    echo "No domain specified: using IPS-PILGRIMAGE"
    domain=IPS-PILGRIMAGE
else
    domain=$3
fi

subdir=$1
desc_dir=$2

GROUP_DESC="DESC"

openssl x509 -outform der -in ${desc_dir}/DESC.pem -out ${desc_dir}/DESC.der
openssl cms -sign -nodetach -in ${desc_dir}/DESC.der -signer ${subdir}/UP.pem -inkey ${subdir}/UP.key -out ${desc_dir}/DESC_cms.der -outform DER -binary
openssl enc -base64 -in ${desc_dir}/DESC_cms.der -e -A > ${desc_dir}/DESC_cms.b64
#openssl x509 -in ${subdir}/DESC.pem -noout -fingerprint -sha256 | sed 's/://g'
payload=$(cat ${desc_dir}/DESC_cms.b64)

curl --location 'https://tng-dev.who.int/trustedCertificate' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{"cms": "'"${payload}"'", "properties": {}, "domain": "'"${domain}"'", "group": "'"${GROUP_DESC}"'"}' \
--key ${subdir}/TLS.key \
--cert ${subdir}/TLS.pem \

#cleanup
rm ${desc_dir}/DESC.der
rm ${desc_dir}/DESC_cms.der
rm ${desc_dir}/DESC_cms.b64

