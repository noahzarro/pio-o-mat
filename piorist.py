# piorist
import json

# returns None if piorist not found
def get_piorist(user_id):
    response = None
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["card_id"]) == user_id:
            response=piorist
    return response


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
            piorists.append({"card_id" : i, "name": name, "vulgo": vulgo, "balance": 0, "statistic": 0, "today": 0})
            break
        i += 1


    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    return i


def delete_piorist(user_id):
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)

    for piorist in piorists:
        if int(piorist["card_id"])==user_id:
            piorists.remove(piorist)

    with open("list.pio", "w") as write_file:
        json.dump(piorists, write_file)
