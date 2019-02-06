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

print(new_menu)