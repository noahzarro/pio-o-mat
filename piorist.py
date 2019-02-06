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
        return dict({"name":self.name,"title":self.vulgo,"back":self.card_id,"sub":self.balance})


def create_piorist(name, vulgo):
    ids = set()
    with open("Piorists/list.pio", "r") as read_file:
        piorists = json.load(read_file)
        for piorist in piorists:
            ids.add(piorist["card_id"])

    i = 1
    while True:
        i += 1
        if not ids.__contains__(i):
            new_piorist = Piorist(i,name,vulgo)
            piorists.add(new_piorist)

    with open("Piorists/list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return new_piorist.card_id
