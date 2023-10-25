#!/bin/zsh

if [ $# -ne 1 ]; then
    echo "Usage: $0 <subdir> (which must exist)"
    exit 1
fi
subdir=$1

DAYS_DSC=730

#openssl req -newkey ec:<(openssl ecparam -name prime256v1) -keyout ${subdir}/DSC.key -nodes -out ${subdir}/DSC_csr.pem -config DSC.conf  # this does only work on Linux/MacOS
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout ${subdir}/DSC.key -nodes -out ${subdir}/DSC_csr.pem -config DSC.conf
openssl x509 -req -in ${subdir}/DSC_csr.pem -CA ${subdir}/SCA.pem -CAkey ${subdir}/SCA.key -CAcreateserial -days ${DAYS_DSC} -extensions ext -extfile DSC.conf -out ${subdir}/DSC.pem
# cleanup
rm ${subdir}/DSC_csr.pem


