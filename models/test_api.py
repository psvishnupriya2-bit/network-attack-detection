import json
import urllib.request

data = json.load(open("models/sample_request.json"))

req = urllib.request.Request(
    "http://127.0.0.1:8000/predict",
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"},
)

print(urllib.request.urlopen(req).read().decode())