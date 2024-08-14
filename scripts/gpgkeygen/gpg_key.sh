#!/bin/bash

# Check for gpg installation
if ! command -v gpg &> /dev/null; then
    echo "gpg could not be found, please install it first."
    exit 1
fi

# Prompt user for name and email
read -p "Enter your name: " NAME_REAL
read -p "Enter your email: " NAME_EMAIL
read -s -p "Enter a pass phrase: " PASS_PHRASE

# Set default values for key generation
KEY_TYPE="RSA"
KEY_LENGTH="4096"
SUBKEY_TYPE="RSA"
SUBKEY_LENGTH="4096"
EXPIRATION_DATE="0" # 0 means key does not expire
#NAME_REAL="John Doe"
#NAME_EMAIL="john.doe@example.com"
NAME_COMMENT="Generated by shell script"

# Create a temporary batch file for key generation
GPG_BATCH=$(mktemp)
cat > "$GPG_BATCH" <<EOF
    %echo Generating a basic OpenPGP key
    Key-Type: $KEY_TYPE
    Key-Length: $KEY_LENGTH
    Subkey-Type: $SUBKEY_TYPE
    Subkey-Length: $SUBKEY_LENGTH
    Name-Real: $NAME_REAL
    Name-Comment: $NAME_COMMENT
    Name-Email: $NAME_EMAIL
    Expire-Date: $EXPIRATION_DATE
    Passphrase: $PASS_PHRASE
    Key-Usage: sign,cert
    %commit
    %echo done
EOF

# Generate the GPG key
gpg --batch --gen-key "$GPG_BATCH"

# Clean up the batch file
rm "$GPG_BATCH"

echo "GPG key generation completed."

# Extract and display the key ID
#KEY_ID=$(gpg --list-keys --with-colons "$NAME_EMAIL" | awk -F: '/^pub/{print $5; exit}')
KEY_ID=$(gpg --list-secret-keys --with-colons "$NAME_EMAIL" | awk -F: '/^sec/ {print $5, $6}' | sort -k2 -nr | head -n1 | awk '{print $1}')
echo "GPG key generation completed. Your key ID is: $KEY_ID"


# Export the public key to a file
OUTPUT_FILE="gpg_key_$KEY_ID.txt"
gpg --armor --export "$KEY_ID" > "$OUTPUT_FILE"
echo "Your public key has been saved to $OUTPUT_FILE"
