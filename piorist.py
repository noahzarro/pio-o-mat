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
                    # does this work?
                    piorist["card_id"] = i
            break
        i += 1

    with open("list.pio", "w") as write_file:
        json.dump(piorists, write_file)

    return i


def set_piorist(new_piorist):
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        # do card_id check:
        if int(piorist["card_id"]) != 0 and int(piorist["card_id"]) != -1:
            if piorist["card_id"] == new_piorist["card_id"]:
                piorists.remove(piorist)
                piorists.append(new_piorist)
                break

        # do swiss_id check:
        if piorist["swiss_id"] != "":
            if piorist["swiss_id"] == new_piorist["swiss_id"]:
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
        if i not in ids:
            piorists.append({"card_id" : i, "swiss_id": "", "name": name, "vulgo": vulgo, "balance": 0, "statistic": 0, "today": 0})
            break
        i += 1


    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return i


def create_piorist_swiss_pass(name, vulgo, swiss_id):
    print(swiss_id)
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)

    for piorist in piorists:
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


