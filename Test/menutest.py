import json
import Menu

# load all menus
menus = {}
menu_list = []
with open("Menus/list.menu", "r") as list_file:
    menu_list = json.load(list_file)
    for menu_name in menu_list:
        with open("Menus/" + menu_name + ".json", "r") as menu_file:
            menu_dict = json.load(menu_file)
            menus[menu_dict["name"]] = Menu.Menu(menu_dict)

for key in menus:
    print(menus[key].name)
