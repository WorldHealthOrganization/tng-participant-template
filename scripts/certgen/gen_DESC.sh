#!/bin/zsh
# this script generates digital signing certificates (DSC)
# the DN is taken from the configuration file passed as argument
# the DSC is generated beneath the directory passed as argument, a new on on each run
# as third parameter, the purpose of the DSC can be passed, e.g. test, vax, rec
# for test, vaccination, and recovery. Omitting the third parameter will result in
# a DSC that can be used for all purposes
# -----------------------------------------------------------------

# DESC is valid for 2 years
VAL_DAYS_DESC=730

if [ $# -lt 2 ]; then
    echo "Usage: $0 <DN_template.cnf> <subdir> (where <subdir> must contain DECA.pem and DECA.key)"
    exit 1
fi

subdir=$2
desc_dir=${subdir}/DESC_$(date +%Y%m%d%H%M%S)
mkdir -p ${desc_dir}

# source the DN from the given configuration file (DN_template.cnf is an example)
source $1

# First create a new private key and a CSR. Note that the keyoptions are hardcoded to prime256v1 curve.
# Use 'openssl ecparam -list_curves' to get a full list of EC curves.
# To use RSA, replace '-newkey ec' with '-newkey rsa' and substitute the 'ec_paramgen_curve' option with 'rsa_keygen_bits:<keysize>'

openssl req -new -newkey ec -pkeyopt ec_paramgen_curve:prime256v1 -keyout ${desc_dir}/DESC.key -nodes -out ${desc_dir}/DESC_csr.pem -config DESC.conf

# ...then sign the CSR with the DECA resulting in a desc
openssl x509 -req -in ${desc_dir}/DESC_csr.pem -CA ${subdir}/DECA.pem -CAkey ${subdir}/DECA.key -CAcreateserial -days ${VAL_DAYS_DESC} -extensions ext -extfile DESC.conf -out ${desc_dir}/DESC.pem

# cleanup the intermediate CSR file
rm ${desc_dir}/DESC_csr.pem


