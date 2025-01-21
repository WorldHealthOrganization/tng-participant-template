#!/bin/bash

#naming conventions
TRUSTED_ISSUER_FILENAME_PATTERN="Trusted_Issuer"
TRUSTED_ISSUER_FOLDER_NAME="ISSUER"


# Check if parameters are provided
if [ $# -ne 3 ]; then
  echo "Usage: $0 <SIGNINGCA> <SIGNINGKEY> <COUNTRY>"
  exit 1
fi

SIGNINGCA="$1"
SIGNINGKEY="$2"
COUNTRY="$3"

# Check if the provided files exist
if [ ! -f "$SIGNINGCA" ] || [ ! -f "$SIGNINGKEY" ]; then
  echo "TNG_TA signing keys not found as $SIGNINGCA and $SIGNINGKEY"
  exit 1
fi

echo "Checking trusted issuer files for country $COUNTRY"
countdirectories=0

# Find all subdirectories named "ISSUER", if for the provided country
for dir in $(find . -type d -name $TRUSTED_ISSUER_FOLDER_NAME | grep $COUNTRY); do

  # Initialize a file signing counter
  countfiles=0

  #for all files in the directory containing the file name pattern excluding the already signed files
  for file in $(find $dir -type f -name *$TRUSTED_ISSUER_FILENAME_PATTERN* | grep -v 'TNG_TA\.signed'); do

    file_name=$(basename "$file")
    #echo "$file_name"

    # Define the JSON input
    json_file="$file"

    # Prepare output folder
    mkdir -p $dir/signed

    # Read the JSON content from the file
    json_input=$(cat "$json_file")
    # Extract values and concatenate with semicolons
    name=$(echo "$json_input" | jq -r '.name')
    url=$(echo "$json_input" | jq -r '.url')
    urlType=$(echo "$json_input" | jq -r '.urlType')
    hash=$(echo "$json_input" | jq -r '.hash')
    alpha2country=$(echo "$json_input" | jq -r '.country')
    # Extract and concatenate sslPublicKeys into one line
    sslPublicKeys=$(echo "$json_input" | jq -r '.sslPublicKeys | join(";")')

    # Print the values separated by semicolons
    # the order of the fields is important and should be the same as in TNG TrustedIssuerService.getHashData()
    signatureInput=$(echo -n "$alpha2country;$name;$url;$urlType")
    echo -n "$signatureInput" > $dir/signed/trusted_issuer_signature_input.txt

    # Create a signature of the input using the signing key
    openssl cms -sign -nodetach -in $dir/signed/trusted_issuer_signature_input.txt -signer $SIGNINGCA -inkey $SIGNINGKEY -out $dir/signed/signature.der -outform DER -binary
    openssl enc -base64 -in $dir/signed/signature.der  -e -a -A > $dir/signed/signature_b64.txt

    # Add the "signature" field to the JSON
    updated_json=$(echo "$json_input" | jq --arg signature "$(cat $dir/signed/signature_b64.txt)" '. + { "signature": $signature }')
    echo "$updated_json" > "$dir/signed/TNG_TA.signed.$file_name"

    #log success
    echo "Signed JSON file output: $dir/signed/TNG_TA.signed.$file_name"

    #cleanup
    rm $dir/signed/signature.der
    rm $dir/signed/signature_b64.txt
    rm $dir/signed/trusted_issuer_signature_input.txt

    # Increment the counter
    ((countfiles++))
  done

  # Print the count and a message if count is 0
  if [ $countfiles -eq 0 ]; then
    echo "No file matching $TRUSTED_ISSUER_FILENAME_PATTERN found for $COUNTRY"
  else
    echo "Signed $countfiles file(s) for country $COUNTRY"
  fi

  # Increment the counter
  ((countdirectories++))
done

echo "Found $countdirectories directory(ies) matching $TRUSTED_ISSUER_FOLDER_NAME for country $COUNTRY"

