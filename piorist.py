# piorist
import json

# returns None if piorist not found
def get_piorist(user_id):
    response = None
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["card_id"]) == user_id or piorist["swiss_id"] == user_id:
            response=piorist
    return response


def add_card_id_to_swiss_id(swiss_id):
    ids = set()
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
        for piorist in piorists:
            ids.add(piorist["card_id"])

    i = 1
    while True:
        if not i in ids:
            for piorist in piorists:
                if piorist["swiss_id"] == swiss_id:
                    piorists["card_id"] = i
            break
        i += 1

    with open("list.pio", "w") as write_file:
        json.dump(piorists, write_file)

    return i


def set_piorist(new_piorist):
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["card_id"]) == int(new_piorist["card_id"]):
            piorists.remove(piorist)
            piorists.append(new_piorist)
            break
    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)


def create_piorist(name, vulgo):
    ids = set()
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
        for piorist in piorists:
            ids.add(piorist["card_id"])

    i = 1
    while True:
        if not i in ids:
            piorists.append({"card_id" : i, "swiss_id": "", "name": name, "vulgo": vulgo, "balance": 0, "statistic": 0, "today": 0})
            break
        i += 1


    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return i


def create_piorist_swiss_pass(name, vulgo, swiss_id):
    ids = set()
    swiss_id = swiss_id.decode('latin_1')
    print(swiss_id)
    swiss_id = swiss_id.encode(encoding='UTF-8',errors='backslashreplace')
    print(swiss_id)
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)

    for piorist in piorists:
        print(type(swiss_id))
        print(type(piorist["swiss_id"]))
        if swiss_id == piorist["swiss_id"]:
            return "in use"

    piorists.append({"card_id" : -1, "swiss_id": swiss_id, "name": name, "vulgo": vulgo, "balance": 0, "statistic": 0, "today": 0})

    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return "ok"


def delete_piorist(user_id):
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)

    for piorist in piorists:
        if int(piorist["card_id"])==user_id or piorist["swiss_id"] == user_id:
            piorists.remove(piorist)

    with open("list.pio", "w") as write_file:
        json.dump(piorists, write_file)
