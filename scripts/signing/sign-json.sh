#!/usr/bin/env bash
set -e

REALPATH=/bin/realpath
BASENAME=/usr/bin/basename
DIRNAME=/usr/bin/dirname
SED=$(type -p sed)
HEAD=$(type -p head)

#signs keys assuming a directory structure as follows
# $ISO3/ – three letter country code or WHO which contains key material
# $ISO3/signing/ – used to contain public keys for signing.  Intended only for use by WHO
# $ISO3/signing/$DOMAIN/$USAGE/$FILEROOT.pem – public key used to verify 
# $ISO3/onboarding/ – used to contain public keys for key material from participants
# $ISO3/onboarding/$DOMAIN/$USAGEDIR
# $ISO3/onboarding/$DOMAIN/$USAGEDIR/$FILEROOT.pem
# $ISO3/onboarding/$DOMAIN/$USAGEDIR/signed/
# $ISO3/onboarding/$DOMAIN/$USAGEDIR/signed/WWO_$USAGE.signed.$FILEROOT.pem
# $ISO3/onboarding/$DOMAIN/$USAGEDIR/signed/WHO_$USAGE.signed.$FILEROOT.txt
#
# each $USAGEDIR should map to a functional CA (e.g. TA, TLS) as defined by $DIRTOUSAGE
#
# also produces a .txt file for databse import to TNG Gateway with following fields
# TrustAnchor Signature:
# Certificate Raw Data: (no BEGIN CERT or END CERT)
# Certificate Thumbprint:
# Certificate Country: 

CASDIR=$1
COUNTRY=$2
if [[ ! -d $CASDIR ]]; then
    echo "Usage: ${BASH_SOURCE[0]} /path/to/private/key/directory"
    echo "       Missing first parameter is path to directory containing private keys"
    exit 1
fi
CASDIR=$($REALPATH ${CASDIR})

KEYTYPESTOSIGN=("onboarding")
CURRDIR=$PWD

declare -A USAGETOSIGNINGCA=(
# [TLS]="$CASDIR/cas/TLS/certs/TNG_TLS.pem"
 [TLS]="$CASDIR/cas/TA/certs/TNG_TA.pem"
 [TA]="$CASDIR/cas/TA/certs/TNG_TA.pem"
)
declare -A USAGETOSIGNINGKEY=(
 #[TLS]="$CASDIR/cas/TLS/private/TNG_TLS.key.pem"	
 [TLS]="$CASDIR/cas/TA/private/TNG_TA.key.pem"
 [TA]="$CASDIR/cas/TA/private/TNG_TA.key.pem"
)
declare -A USAGETOSIGNINGCFG=(
 #[TLS]="$CASDIR/cas/TLS/openssl.conf"
 [TLS]="$CASDIR/cas/TA/openssl.conf"
 [TA]="$CASDIR/cas/TA/openssl.conf"
 )

declare -A DIRTOUSAGE=(
  [auth]="TLS"
  [AUTH]="TLS"
  [TLS]="TA"
  [tls]="TA"
  [up]="TA"
  [UP]="TA"
  [csca]="TA"
  [CSCA]="TA"
  [sca]="TA"
  [SCA]="TA"
)
EXCLUDEFROMSIGNING=("CA")

function exists_in_list() { # call: list, item-delimter, value-to-compare
    LIST=$1
    DELIMITER=$2
    VALUE=$3
    [[ "$LIST" =~ ($DELIMITER|^)$VALUE($DELIMITER|$) ]]
}

#ROOT=$($REALPATH $(dirname $(dirname $(dirname ${BASH_SOURCE[0]}))))
echo "Examining contents of $CURRDIR";
for DIR in $CURRDIR/*
do
    if [[ ! -d $DIR || -L $DIR ]]; then continue; fi #not a directory 
    ISO3=$($BASENAME "$DIR")
    if [[ "${ISO3}" == "WHO" ]]; then continue; fi #Skip WHO keys
    echo "Processing Folder: ${ISO3}"

    if [[ ! -z $COUNTRY && $COUNTRY != $ISO3 ]]; then continue; fi # skip countries 
    
    for KEYDIR in $DIR/*
    do
	if [[ ! -d $KEYDIR || -L $KEYDIR ]]; then continue; fi #not a directory 
	KEYTYPE=$($BASENAME "$KEYDIR")
	if [[ ! ${KEYTYPESTOSIGN[@]} =~ $KEYTYPE ]]; then continue; fi
	echo "  Found Key Type: $KEYTYPE";

	for DOMAINDIR in $KEYDIR/*		     
	do
	    if [[ ! -d $DOMAINDIR ||  -L $DOMAINDIR ]]; then continue; fi #not a directory 
	    DOMAIN=$($BASENAME "$DOMAINDIR")
	    echo "    Found Domain: $DOMAIN";
	    for USAGEDIR in $DOMAINDIR/*/
	    do
		
		if [[ ! -d $USAGEDIR ||  -L $USAGEDIR ]]; then continue; fi #not a directory 
		USAGEDIR=$($BASENAME "$USAGEDIR")

		if [ ! "${DIRTOUSAGE[$USAGEDIR]+isset}" ]; then
		    #don't know what to sign with
		    echo "    Don't know what type of keys are in $USAGEDIR"
		    continue
		fi 
		USAGE=${DIRTOUSAGE[$USAGEDIR]}
		USAGEDIR=$DOMAINDIR/$USAGEDIR
		#echo "DD="$DOMAINDIR
		#echo "UD="$USAGEDIR
		if [ ! "${USAGETOSIGNINGKEY[$USAGE]+isset}" ]; then
		    echo "    Don't know what to sign keys in $USAGEDIR with"
		    #don't know what to sign with
		    continue
		fi
		SIGNINGKEY=$PRIVATEKEYDIR/${USAGETOSIGNINGKEY[$USAGE]}
		SIGNINGCA=$PRIVATEKEYDIR/${USAGETOSIGNINGCA[$USAGE]}
		SIGNINGCFG=$PRIVATEKEYDIR/${USAGETOSIGNINGCFG[$USAGE]}
		if [ ! -e "$SIGNINGKEY" ]; then
		    echo "Error: Could not find $SIGNINGKEY"
		    exit 2
		fi;
		echo "      Found Key Usage: $USAGE signing with $SIGNINGKEY";
		SIGNEDDIR=$USAGEDIR/signed
		echo Creating signing directory: "$SIGNEDDIR"
		mkdir -p $SIGNEDDIR

		for CERTPATH in $USAGEDIR/*.pem
		do
		    CERT=$($BASENAME "${CERTPATH}")
		    CERTPATHCOMP=$($DIRNAME "${CERTPATH}")
		    SIGNEDCERT=signed.$CERT
		    CSR=$CERT.csr
		    SIGNEDTXT=TNG_$USAGE.signed.${CERT%.pem}.json
		    SIGNEDCERTPATH=$SIGNEDDIR/$SIGNEDCERT
		    SIGNEDTXTPATH=$SIGNEDDIR/$SIGNEDTXT
		    CSRPATH=$SIGNEDDIR/$CSR

		    if exists_in_list $EXCLUDEFROMSIGNING "," ${CERT%.pem}; then
			echo "         Found $CERT ...excluding it from signing"
			continue
		    fi

		    echo "        Signing CERT $CERT with $SIGNINGCA "
		    echo "           x509 Output At: $SIGNEDCERTPATH"

		    cd $CASDIR
		    # SUBJ=$(openssl x509 -in ${CERTPATH} -noout -subject --nameopt multiline | tail -n +2 | $SED 's/^\s*/\//' | $SED 's/\s*=\s*/=/' |$SED -z 's/\n//g')
		    # openssl req -out ${CSRPATH} -key ${SIGNINGKEY} -new  -subj "${SUBJ}" 
		    # openssl ca -batch -create_serial -config $SIGNINGCFG -cert $SIGNINGCA -keyfile $SIGNINGKEY \
			#     -in $CSRPATH -out $SIGNEDCERTPATH   -subj "${SUBJ}"  2>&1 | $SED 's/^/            | /g'
		    cd $CURRDIR


		    COUNTRYNAME=`openssl x509 -in ${CERTPATH} -noout -subject -nameopt multiline | grep countryName | awk -F'=' '{print $2}'  | $SED 's/\s*//'`
		    if [ ! -z ${COUNTRYNAME} ]; then
			echo "           JSON Output At ${COUNTRYNAME}: $SIGNEDTXTPATH"
			echo '{' > $SIGNEDTXTPATH
			echo -n '"trustAnchorSignature": "' >> $SIGNEDTXTPATH
			#echo `openssl x509 -outform der -inform $CERT -out $SIGNEDDIR/${CERT}.der`
			openssl x509 -outform der -in ${CERTPATH} -out $SIGNEDDIR/${CERT}.der
			openssl cms -sign -nodetach -in $SIGNEDDIR/${CERT}.der -signer $SIGNINGCA -inkey $SIGNINGKEY -out $SIGNEDDIR/${CERT}_signed.der -outform DER -binary
			#echo `openssl base64 in $SIGNEDDIR/${CERT}_signed.der -out -out signed.b64 -e -A`
			echo -n `openssl enc -base64 -in $SIGNEDDIR/${CERT}_signed.der  -e -a -A | $SED -z 's/\n*//g' | $SED -z 's/\s*//g' ` \
			     >>  $SIGNEDTXTPATH
			echo '",' >>  $SIGNEDTXTPATH
			#	echo `openssl x509 -in ${SIGNEDCERTPATH} -outform DER -fingerprint -sha256 -noout | awk -F'=' '{print $2}'  | $SED 's/://g' | $SED 's/[A-Z]/\L&/g'` \
			    #>>  $SIGNEDTXTPATH
			echo -n  '"certificateRawData": "' >> $SIGNEDTXTPATH
			echo -n `openssl x509 -in ${CERTPATH}  | tail -n +2 | $HEAD -n -1 | $SED -z 's/\n*//g' | $SED -z 's/\s*//g' ` \
			     >> $SIGNEDTXTPATH
			echo '",' >>  $SIGNEDTXTPATH
			echo -n '"certificateThumbprint": "' >>  $SIGNEDTXTPATH
			echo -n `openssl x509 -in ${CERTPATH} -fingerprint -sha256 -noout | awk -F'=' '{print $2}' | $SED 's/://g' | $SED 's/[A-Z]/\L&/g' ` \
			     >>  $SIGNEDTXTPATH
			echo '",' >>  $SIGNEDTXTPATH
			echo -n '"country": "'$COUNTRYNAME \
			     >>  $SIGNEDTXTPATH
			echo '"' >>  $SIGNEDTXTPATH
			echo -n '}' >>  $SIGNEDTXTPATH
			# cleanup
		    else 
			echo "           Skipping Text Output"
		    fi
		    # clean up temporary data
		    for delTMP in ${CERTPATHCOMP}/signed/*.der ${CERTPATHCOMP}/signed/*.csr ${CERTPATHCOMP}/*.csr ; do
			echo not cleaning up... $delTMP
			#rm -rf $delTMP
		    done
		done

		for CERTPATH in $USAGEDIR/UP_SYNC.csr
		do
		    if [[ ! -e $CERTPATH ]]; then continue; fi
		    CERT=$($BASENAME "${CERTPATH}")
		    CERTNAME=$($BASENAME -s csr "${CERTPATH}")
		    CERTPATHCOMP=$($DIRNAME "${CERTPATH}")
		    SIGNEDCERT=signed.$CERT.pem
		    CSR=$CERT.CSR
		    SIGNEDTXT=TNG_$USAGE.signed.${CERT%.pem}.json
		    SIGNEDCERTPATH=$SIGNEDDIR/$SIGNEDCERT
		    SIGNEDTXTPATH=$SIGNEDDIR/$SIGNEDTXT
		    CSRPATH=$SIGNEDDIR/$CSR
		    echo "        Signing UP_SYNC_CERT $KEY with $SIGNINGCA "
		    echo "           x509 Output At: $SIGNEDCERTPATH"
		    cd $CASDIR
		    #SUBJ=$(openssl x509 -in ${CERTPATH} -noout -subject --nameopt multiline | tail -n +2 | $SED 's/^\s*/\//' | $SED 's/\s*=\s*/=/' |$SED -z 's/\n//g')
		    SUBJ="/C=${COUNTRYNAME}/CN=UP_SYNC_CERT_SIGNING/O=WHO/OU=WHO_TA"
		    # openssl req -out ${CSRPATH} -key ${SIGNINGKEY} -new  -subj "${SUBJ}" 
		    openssl ca -batch -create_serial -notext -config $SIGNINGCFG -cert $SIGNINGCA -keyfile $SIGNINGKEY \
			    -in $CERTPATH -out $SIGNEDCERTPATH -preserveDN  2>&1 | $SED 's/^/            | /g'
		    cd $CURRDIR
		    echo copy $SIGNEDCERTPATH to $CERTPATHCOMP/${CERTNAME}pem
		    cp $SIGNEDCERTPATH $CERTPATHCOMP/${CERTNAME}pem
		    #     COUNTRYNAME=`openssl x509 -in ${CERTPATH} -noout -subject -nameopt multiline | grep countryName | awk -F'=' '{print $2}'  | $SED 's/\s*//'`
		    #     if [ ! -z ${COUNTRYNAME} ]; then
		    # 	echo "           Text Output At ${COUNTRYNAME}: $SIGNEDTXTPATH"
		    echo '{' > $SIGNEDTXTPATH
		    echo -n '"trustAnchorSignature": "' >> $SIGNEDTXTPATH
	 	    openssl x509 -outform der -in ${SIGNEDCERTPATH} -out $SIGNEDDIR/${CERT}.der
		    openssl cms -sign -nodetach -in $SIGNEDDIR/${CERT}.der -signer $SIGNINGCA -inkey $SIGNINGKEY -out $SIGNEDDIR/${CERT}_signed.der -outform DER -binary
		    echo -n `openssl enc -base64 -in $SIGNEDDIR/${CERT}_signed.der  -e -a -A | $SED -z 's/\n*//g' | $SED -z 's/\s*//g' ` >>  $SIGNEDTXTPATH
		    echo '",' >>  $SIGNEDTXTPATH
	 	    echo -n  '"certificateRawData": "' >> $SIGNEDTXTPATH
	 	    echo -n `openssl x509 -in ${SIGNEDCERTPATH}  | tail -n +2 | $HEAD -n -1 | $SED -z 's/\n*//g' | $SED -z 's/\s*//g' ` >> $SIGNEDTXTPATH
		    echo '",' >>  $SIGNEDTXTPATH
		    echo -n '"certificateThumbprint": "' >>  $SIGNEDTXTPATH
		    echo -n  `openssl x509 -in ${SIGNEDCERTPATH} -fingerprint -sha256 -noout | awk -F'=' '{print $2}' | $SED 's/://g' | $SED 's/[A-Z]/\L&/g' ` >>  $SIGNEDTXTPATH
		    echo '",' >>  $SIGNEDTXTPATH
		    echo -n '"country": "'$COUNTRYNAME \
			 >>  $SIGNEDTXTPATH
		    echo '"' >>  $SIGNEDTXTPATH
		    echo -n '}' >>  $SIGNEDTXTPATH
		    echo move $SIGNEDCERTPATH to $CERTPATHCOMP/${CERTNAME}pem
		    mv $SIGNEDCERTPATH $CERTPATHCOMP/${CERTNAME}pem # move signed pem
		    # clean up temporary data
		    for delTMP in ${CERTPATHCOMP}/signed/*.der ${CERTPATHCOMP}/signed/*.csr ${CERTPATHCOMP}/*.csr ; do
		 	#echo cleaning up... $delTMP
		 	rm -rf $delTMP
		    done

		    #     else 
		    # 	echo "           Skipping Text Output"
		    #     fi
		done
	    done
	done
    done
done
