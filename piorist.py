# piorist
import json

class Piorist:
    card_id = 0
    name = ""
    vulgo = ""
    balance = 0.0

    def __init__(self, card_id, name, vulgo):
        self.card_id = card_id
        self.name = name
        self.vulgo = vulgo
        self.balance = 0.0

    def to_dict(self):
        return dict({"name":self.name,"vulgo":self.vulgo,"card_id":self.card_id,"balance":self.balance})

def pay_pio(user_id,pio_preis):
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["card_id"])==user_id:
            if piorist["balance"] >= pio_preis:
                piorist["balance"] -= pio_preis
                with open("list.pio", "w") as write_file:
                    json.dump(piorists, write_file)
                return "zum Wohl,"
            else:
                with open("list.pio", "w") as write_file:
                    json.dump(piorists, write_file)
                return "Saldo zu klein"
    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)
    return "nicht registriert"

def create_piorist(name, vulgo):
    ids = set()
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
        for piorist in piorists:
            ids.add(piorist["card_id"])

    i = 1
    while True:
        if not i in ids:
            new_piorist = Piorist(i,name,vulgo)
            piorists.append(new_piorist.to_dict())
            break
        i += 1


    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return new_piorist.card_id
