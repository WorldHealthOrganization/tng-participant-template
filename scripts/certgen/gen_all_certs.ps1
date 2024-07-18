# valid for 4 years
$DAYS_CA=1461
# valid for 1 year
$DAYS_TLS=365
# valid for 1 year
$DAYS_UPLOAD=365

# configure the DN
$env:OSSL_COUNTRY_NAME="XA"
$env:OSSL_STATE_NAME="Test State"
$env:OSSL_LOCALITY_NAME="Geneva"
$env:OSSL_ORGANIZATION_NAME="WHO"
$env:OSSL_ORGANIZATIONAL_UNIT_NAME="R&D"
# $env:OSSL_COMMON_NAME="WHO International" # default entry of the corresponding config file will be used

# generate a new directory for each run
$subdir = Get-Date -Format "yyyyMMddHHmmss"
New-Item -ItemType Directory -Force -Path $subdir

# generate the certificates and keys for the SCA, TLS, and upload
openssl ecparam -name prime256v1 -out ecparam.pem
openssl req -x509 -new -days $DAYS_CA -newkey ec:ecparam.pem -extensions ext -keyout $subdir/SCA.key -nodes -out $subdir/SCA.pem -config sca.conf
openssl req -x509 -new -days $DAYS_TLS -newkey ec:ecparam.pem -extensions ext -keyout $subdir/TLS.key -nodes -out $subdir/TLS.pem -config TLSClient.conf
openssl req -x509 -new -days $DAYS_UPLOAD -newkey ec:ecparam.pem -extensions ext -keyout $subdir/UP.key -nodes -out $subdir/UP.pem -config uploadCert.conf
rm ecparam.pem
# special case to only place CA.pem file for self-signed TLS cert as a copy
Copy-Item -Path $subdir/TLS.pem -Destination $subdir/CA.pem
