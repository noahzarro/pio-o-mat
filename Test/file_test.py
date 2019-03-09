import json
import requests

import random
import string

url = "http://people.ee.ethz.ch/~zarron/send_statistic.php"

# load passwort
with open("password.json", "r") as read_file:
    password = json.load(read_file)[0]

# load data for statistic
with open("list.pio", "r") as read_file:
    piorists = json.load(read_file)

vulgo = []
statistic = []
today = []

for piorist in piorists:
    vulgo.append(piorist["vulgo"])
    statistic.append(piorist["statistic"])
    today.append(piorist["today"])

data = {"vulgo": vulgo, "statistic": statistic, "today": today}

# generate authentication token
auth = ""
for i in range(0, 6):
    auth += random.choice(string.ascii_uppercase + string.digits)

print(auth)

payload = {"password": password, "auth": auth, "data": json.dumps(data)}

print(data)
print(type(data))

# send data
try:
    r = requests.post(url, data=payload)
    print(r.text)
except:
    print("keine Verbindung")
