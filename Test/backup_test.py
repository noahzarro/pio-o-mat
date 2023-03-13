import json
import requests

url = "http://people.ee.ethz.ch/~zarron/backup.php"

with open("gitter.txt", "r") as read_file:
    payload_string = json.dumps(json.load(read_file))

payload = {"load": payload_string}

r = requests.post(url, data=payload)

print(r.text)
