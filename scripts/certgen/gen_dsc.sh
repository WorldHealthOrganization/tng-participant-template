#!/bin/zsh
# this script generates digital signing certificates (DSC)
# the DN is taken from the configuration file passed as argument
# the DSC is generated beneath the directory passed as argument, a new on on each run
# as third parameter, the purpose of the DSC can be passed, e.g. test, vax, rec
# for test, vaccination, and recovery. Omitting the third parameter will result in
# a DSC that can be used for all purposes
# -----------------------------------------------------------------

# DSC is valid for 2 years
DAYS_DSC=730

if [ $# -lt 2 ]; then
    echo "Usage: $0 <template.cnf> <subdir> (where <subdir> must contain SCA.pem and SCA.key) [test|vax|rec]"
    exit 1
fi
if [ -z $3 ]; then
    ext=all
else
    ext=$3
fi

subdir=$2
dsc_dir=${subdir}/DSC_$(date +%Y%m%d%H%M%S)
mkdir -p ${dsc_dir}
source $1

#openssl req -newkey ec:<(openssl ecparam -name prime256v1) -keyout ${subdir}/DSC.key -nodes -out ${subdir}/DSC_csr.pem -config DSC.conf  # this does only work on Linux/MacOS
openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout ${dsc_dir}/DSC.key -nodes -out ${dsc_dir}/DSC_csr.pem -config DSC.conf
openssl x509 -req -in ${dsc_dir}/DSC_csr.pem -CA ${subdir}/SCA.pem -CAkey ${subdir}/SCA.key -CAcreateserial -days ${DAYS_DSC} -extensions $ext -extfile DSC.conf -out ${dsc_dir}/DSC.pem
# cleanup
rm ${dsc_dir}/DSC_csr.pem


