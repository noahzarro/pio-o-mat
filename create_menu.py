import Menu
import json

# new menu
new_menu = Menu.Menu();

# get name
name = input("set name: ")
new_menu.name = name

# get title
title = input("set title: ")
new_menu.title = title

# get back menu
back = input("set back menu: ")
new_menu.back = back

# get submenus
sub = ""
while True:
    sub = input("set submenu: ")
    if sub == "":
        break;
    new_menu.sub.append(sub)

if not new_menu.sub:
    function = input("set menu function: ")
    new_menu.function = function
else:
    new_menu.function = ""

# save menu
with open("Menus/"+new_menu.name+".json", "w") as write_file:
    dict_menu = new_menu.to_dict()
    json.dump(dict_menu,write_file)

# update menu list
menu_list = []
with open("Menus/list.menu","r") as read_file:
    menu_list = json.load(read_file)

menu_list.append(new_menu.name)
with open("Menus/list.menu","w") as write_file:
    json.dump(menu_list,write_file)
