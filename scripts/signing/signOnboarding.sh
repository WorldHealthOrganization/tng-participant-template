#!/usr/bin/env bash
set -e

# script to be executed from root folder of tng-participants-XXX directory
# script to execute against directory containing signing keys <CASDIR>
# process github  onboardingRequest  branches looking for last commit to have a tag of the format signingRequest-$PCODE-$DATE-$TIME
# where $PCODE is a participant code
# example tag: signingRequest-POL-20231130-135900



BASENAME=/usr/bin/basename
DIRNAME=/usr/bin/dirname
CURRDIR=$PWD
SOURCEDIR=$(realpath $($DIRNAME ${BASH_SOURCE[0]}))
SRCSIGNSCRIPT=$SOURCEDIR/sign-json.sh
SIGNSCRIPT=/tmp/`uuid`.sh
cp "$SRCSIGNSCRIPT" $SIGNSCRIPT
chmod +x $SIGNSCRIPT

echo $SIGNSCRIPT


#ROOT=$(realpath $(dirname $(dirname $(dirname ${BASH_SOURCE[0]}))))
#cd $ROOT


CASDIR=$1
if [[ ! -d $CASDIR ]]; then
    echo "Usage: ${BASH_SOURCE[0]} /path/to/private/key/directory"
    echo "       Missing first parameter is path to directory containing private keys"
    exit 1
fi
CASDIR=$(realpath ${CASDIR})


git switch main
BRANCHES=$(git branch -v  --no-color --list "*/onboardingRequest" "*/resign")
echo Scanning Branches: $BRANCHES
printf '  branch info: %s\n' "${BRANCHES[@]}"

while IFS= read -r BRANCHLIST
do
    BRANCH=$(echo $BRANCHLIST | grep -o '^\S*')
    PCODE=$(echo $BRANCH  | sed 's/\/onboardingRequest//;s/\/resign//')
    echo Checking branch: $BRANCH for $PCODE

    git switch $BRANCH
    set +e
    TAGS=`git log --decorate=full -1 HEAD | head -1 | sed 's/.*(\(.*\))/\1/' | sed -E 's/,[[:space:]]+/\n/g' | grep -o '^tag: refs\/tags\/signingRequest-.*' | grep -o 'signingRequest-.*'`
    set -e
    echo Last commit has following tags: $TAGS
    printf '  tag info: %s\n' "${TAGS[@]}"
    while IFS= read -r TAG
    do
	echo Found signing tag, initiating signature process: $TAG
	$SIGNSCRIPT  "$CASDIR" $PCODE
	git add --dry-run $PCODE
	git add $PCODE
	git commit -m "Signed $PCODE"
	DATE=$(date +%Y%m%d-%H%M%S)
	STAG="signedRequest-$PCODE-$DATE-$RANDOM" 
	git tag "$STAG"
    done <<< "$TAGS"  

done <<< "$BRANCHES"

git switch main    
	


