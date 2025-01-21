#!/usr/bin/env bash
set -e
 
# script to push signed branches to remote
# process github onboardingRequest branches looking for last commit to have a tag of the format signedRequest-$PCODE-$DATE-$TIME 
# where $PCODE is a participant code  
# example tag: signedRequest-POL-20231130-135900

BRANCHES=$(git branch -v  --no-color --list "*/onboardingRequest" --list "*/resign")
echo Scanning Branches: $BRANCHES

while IFS= read -r BRANCHLIST
do
    BRANCH=$(echo $BRANCHLIST | grep -o '^\S*')
    PCODE=$(echo $BRANCH  | sed 's/\/onboardingRequest//;s/\/resign//')
    echo Checking branch: $BRANCH for $PCODE

    git switch $BRANCH
    TAGS=`git log --decorate=full -1 HEAD | head -1 | sed 's/.*(\(.*\))/\1/' | sed -E 's/,[[:space:]]+/\n/g' | grep -o '^tag: refs\/tags\/signedRequest-.*' | grep -o 'signedRequest-.*'`
    echo Last commit has following tags: $TAGS
    while IFS= read -r TAG
    do
	echo "Pushing to remote"
	git push
	git push origin "$TAG"
    done <<< "$TAGS"  

done <<< "$BRANCHES"


git switch main
