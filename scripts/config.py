import os
import json
import base64

with open("temp/base64") as f:
    data = f.read()
    missing_padding = len(data) % 4
    if missing_padding == 3:
        data = data[0:-3]
    elif missing_padding != 0:
        data += '=' * (4 - missing_padding)
    decodedBytes = base64.urlsafe_b64decode(data)
    decodedStr = str(decodedBytes, "utf-8")
d = json.loads(decodedStr, strict=False)

if "sync" in d and d["sync"] == True:
    os.system("touch sync")
else:
    os.system("echo 'https://"+os.environ.get("BOT_TOKEN_GITHUB")+"@"+d["repo"] + "' > temp/repo")
    for key in d["keys"]:          
        os.system("echo '"+key + "' >> temp/gpg")
        
# prepare signing
        
os.system("mkdir -p sign/cas/TA/certs")
os.system("mkdir -p sign/cas/TA/private")
os.system("cp ./scripts/signing/openssl.conf sign/cas/TA/openssl.conf")
os.system("echo '"+os.environ.get("SIGN_TA_PEM")+"' > sign/cas/TA/certs/TNG_TA.pem")
os.system("echo '"+os.environ.get("SIGN_TA_KEY")+"' > sign/cas/TA/private/TNG_TA.key.pem")