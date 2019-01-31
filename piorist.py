# piorist
import datetime
import requests

r = requests.get('http://people.ee.ethz.ch/~zarron/accountAPI.php')
print(r.text)

class Piorist:
    card_id = 0
    name = ""
    vulgo = ""
    balance = 0.0
