#!/bin/bash

echo "Start Transitive Trust"

rm -rf transit
git clone https://$BOT_TOKEN_GITHUB@$TRANSITIVE_TRUST_SOURCE transit
cd transit
cd $ENV
mkdir signing 
cd signing     
echo "$NB_UP_SIGNING_PUB" > pub-key.pem
echo "$NB_UP_SIGNING_KEY" > priv-key.pem
cd .. 
cd ..
./extract.sh $ENV $1     
cd ..
echo "Finished Transitive Trust"
