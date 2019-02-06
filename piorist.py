# piorist

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
