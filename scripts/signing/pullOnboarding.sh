#!/usr/bin/env bash
set -e

#script to scan remote $REMOTE for open pull requests on a branch named $PCODE/onboardingRequest
#which are assigned to $ASSIGNEE
# where $PCODE is a Participant code

REALPATH=/bin/realpath
BASENAME=/usr/bin/basename
DIRNAME=/usr/bin/dirname


ASSIGNEE=$1
if  [[ -z $ASSIGNEE ]]; then
    echo "Usage: ${BASH_SOURCE[0]} <ASSIGNEE>"
    echo "       where <ASSIGNEE> is primary GitHub username assigned to pull request of interest"
    echo "       example ASIGNEE: tng-bot-dev"
    exit 1
fi
ASSIGNEEEMAIL="$1@who.int"


REMOTE=$(git ls-remote --get-url origin | sed 's/^.*://g' | sed 's/\.git$//')
echo Remote: $REMOTE
echo ${BASH_SOURCE[0]}
#ROOT=$($REALPATH $($DIRNAME $($DIRNAME  $($DIRNAME   ${BASH_SOURCE[0]}))))
#cd $ROOT


git switch main
git fetch --all



REFS=$(curl  -H "Accept: application/vnd.github.v3+json" https://api.github.com/repos/$REMOTE/pulls\?state=open \
	   | jq ".[] | select( .assignee.login == \"$ASSIGNEE\").head.ref" \
	   | grep "onboardingRequest\|resign"   \
	   | sed 's/\"//g'
    )
echo "Open Pull Requests for $ASSIGNEE: ${REFS[*]}"

PCODES=()
while IFS= read -r REF
do
    if [[  -z "${REF// }" ]] ; then
	echo "Warning empty reference - may be because no open PRs"
	continue
    fi

    echo Processing PR: "$REF"
    BE=`git branch --list "$REF"`
    if [[ -z $BE ]] ; then
	echo Checking out "$REF"x
	git checkout -b $REF origin/$REF
    else
	echo Switching to "$REF"
	git switch "$REF"
    fi
    git config user.name "$ASSIGNEE"
    git config user.email "$ASSIGNEEEMAIL"
    echo Pulling remote "$REF" 
    git pull
    PCODE=$(echo $REF  | sed 's/\/onboardingRequest//;s/\/resign//')
    PCODES+=($PCODE)
    DATE=$(date +%Y%m%d-%H%M%S)
    TAG="signingRequest-$PCODE-$DATE"
    echo "Tagging $TAG"
    git tag "$TAG"
    git push origin "$TAG"
done <<< "$REFS"

git switch main
echo Please sign on the following partcipants: "${PCODES[*]}"


