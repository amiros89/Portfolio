import json
with open("rsa.pem","r") as f:
    rsa=f.read()

print(json.dumps(rsa))
