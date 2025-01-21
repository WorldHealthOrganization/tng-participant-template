echo "Start Verify"
gpg --import temp/gpg > /dev/null 2>&1
cd repo
cat ../temp/tag | xargs git verify-tag --raw 2>../temp/verifyResultTmp
cat ../temp/verifyResultTmp | grep "GOODSIG" > ../temp/verifyResult
cd ..
gpg --list-keys --with-colons | grep fpr| awk 'NR % 2== 0' | awk -F ':' '{print $10}' | xargs gpg --batch --yes --delete-keys
echo "Finished Verify"