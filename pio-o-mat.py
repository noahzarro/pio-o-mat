#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pio-o-mat, for managing beer consumption at serafins ruemli

from luma.core.interface.serial import spi
from luma.core.render import canvas

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time

from PIL import Image

import SimpleMFRC522

import piorist
import Menu
import GPIO_button
import threading

import json
import requests
import codecs

import random
import string

# function definitions
def display_title(title ,draw):
    draw.rectangle([(0, 0), (128, title_height)], fill="white")
    draw.text((1, 1), title, fill="black")


def draw_menu(device, menu, selection):
    try:
        with canvas(device) as draw:
            # clear everything
            draw.rectangle([(0, 0), (128, 64)], fill="black")
            # draw title
            display_title(menu.title, draw)
            # draw submenus
            i=0
            for submenu in menu.sub:
                draw.text((8,title_height+i*8),menus[submenu].title, fill="white")
                i += 1
            # draw selection
            draw.polygon([(1,title_height+selection*8+2),(1,title_height+selection*8+8),(4,title_height+selection*8+5)], fill="white")
            return 0
    except:
        print("except")
        return 1


class buzzer(threading.Thread):
    def __init__(self, mode):
        self.mode = mode

    def run(self):
        if self.mode == "suc":
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
        elif self.mode == "fail":
            for i in range(0, 5):
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)


class led(threading.Thread):
    def __init__(self, mode):
        self.mode = mode

    def run(self):
        if self.mode == "suc":
            GPIO.output(GREEN_PIN, GPIO.HIGH)
        elif self.mode == "fail":
            GPIO.output(RED_PIN, GPIO.HIGH)
        time.sleep(2)
        clear_output()


def backup():

    url = "http://people.ee.ethz.ch/~zarron/backup.php"

    # load passwort
    with open("password.json", "r") as read_file:
        password = json.load(read_file)[0]

    with open("list.pio", "r") as read_file:
        payload_string = json.dumps(json.load(read_file))

    payload = {"load": payload_string, "password": password}

    try:
        r = requests.post(url, data=payload)
    except:
        with canvas(device) as draw:
            display_title("Backup", draw)
            draw.text((8, title_height), "Keine Verbindung", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    with canvas(device) as draw:
        display_title("Backup", draw)
        draw.text((8, title_height), "Backup erstellt", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def new_account():
    try:
        request = requests.get('http://people.ee.ethz.ch/~zarron/accountAPI.php')
    except:
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "Keine Verbindung", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    account_data = json.loads(request.text)
    with canvas(device) as draw:
        display_title("Neuer Account", draw)
        draw.text((8, title_height), "Name: " + account_data["name"], fill="white")
        draw.text((8, title_height + 8), "Vulgo: " + account_data["vulgo"], fill="white")
        print(account_data["vulgo"])

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    # check if card is empty
    myReader = SimpleMFRC522.SimpleMFRC522()
    r = myReader.read()
    print(r[1])
    if r[1]==empty_card:
        user_id = piorist.create_piorist(account_data["name"],account_data["vulgo"])
        myReader.write(str(user_id))
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "erfolgreich!", fill="white")
    else:
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "Karte bereits", fill="white")
            draw.text((8, title_height+8), "beschrieben", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def new_account_swiss_id():
    try:
        request = requests.get('http://people.ee.ethz.ch/~zarron/accountAPI.php')
    except:
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "Keine Verbindung", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    account_data = json.loads(request.text)
    with canvas(device) as draw:
        display_title("Neuer Account", draw)
        draw.text((8, title_height), "Name: " + account_data["name"], fill="white")
        draw.text((8, title_height + 8), "Vulgo: " + account_data["vulgo"], fill="white")
        print(account_data["vulgo"])

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with canvas(device) as draw:
        display_title("Swisspass", draw)
        draw.text((8, title_height), "Swisspass bitte", fill="white")

    # setup reader
    myReader = SimpleMFRC522.SimpleMFRC522()

    while True:
        # try read swiss_id
        id, read_id = myReader.read_no_block_swiss_pass()
        if id is not None:
            break

        if button_back.pressed():
            return "back", None
        if button_pio.pressed():
            return "pio", None

    print(read_id)

    # check if card is empty
    myReader = SimpleMFRC522.SimpleMFRC522()
    r = myReader.read_swiss_pass()
    print(r[1])
    state = piorist.create_piorist_swiss_pass(account_data["name"],account_data["vulgo"], r[1])

    if state == "ok":
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "erfolgreich!", fill="white")
    if state == "in use":
        with canvas(device) as draw:
            display_title("Neuer Account", draw)
            draw.text((8, title_height), "Swisspass", fill="white")
            draw.text((16, title_height), "bereits in", fill="white")
            draw.text((24, title_height), "Gebrauch", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def clear_output():
    GPIO.output(RED_PIN,GPIO.LOW)
    GPIO.output(GREEN_PIN, GPIO.LOW)


def success():
    GPIO.output(GREEN_PIN,GPIO.HIGH)
    buzzer_thread = buzzer("suc")
    led_thread =  led("suc")
    buzzer_thread.run()
    led_thread.run()


def failure():
    GPIO.output(RED_PIN,GPIO.HIGH)
    buzzer_thread = buzzer("fail")
    led_thread = led("fail")
    buzzer_thread.run()
    led_thread.run()


def read_id():
    action = None

    # setup reader
    myReader = SimpleMFRC522.SimpleMFRC522()

    # read until id got or cancelled
    id, read_id = myReader.read_no_block()
    while True:
        # try read card_id
        id, read_id = myReader.read_no_block()
        if id is not None:
            break

        # try read swiss_id
        id, read_id = myReader.read_no_block_swiss_pass()
        if id is not None:
            break

        if button_back.pressed():
            return "back", None
        if button_pio.pressed():
            return "pio", None

    print(read_id)

    # check whether id is swiss_id or card id
    try:
        user_id = int(read_id)
        print("card_id used")
    except:
        user_id = read_id
        print("swiss_id used")

    return action, user_id


def pio():
    with canvas(device) as draw:
        display_title("Pio", draw)
        draw.text((8, title_height), "Pio Bestellung", fill="white")
        draw.text((8, title_height+8), "Karte bitte", fill="white")

    action, user_id = read_id()
    print(action)
    print(user_id)

    if action is not None:
        return action

    # pay pio and show result

    payer = piorist.get_piorist(user_id)
    if not payer is None:
        if payer["balance"] >= pio_preis:
            response = "Zum Wohl, " + payer["vulgo"]
            payer["balance"] = payer ["balance"] - pio_preis
            payer["statistic"] = payer["statistic"] + 1
            payer["today"] = payer["today"] + 1
            success()
        else:
            response = "Saldo zu klein"
            failure()

        with canvas(device) as draw:
            display_title("Pio", draw)
            draw.text((8, title_height), response, fill="white")
            draw.text((8, title_height + 8), "Kontostand: " + str(payer["balance"]/100.0) + " Fr.", fill="white")

        piorist.set_piorist(payer)

    else:
        with canvas(device) as draw:
            display_title("Pio", draw)
            draw.text((8, title_height), "Benutzer unbekannt", fill="white")
        failure()

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def erase():
    with canvas(device) as draw:
        display_title("Karte formatieren", draw)
        draw.text((8, title_height), "Karte bitte", fill="white")

    action, user_id = read_id()
    if action is not None:
        return action

    # check if user exists do not delete
    user = piorist.get_piorist(user_id)
    if user is not None:
        with canvas(device) as draw:
            display_title("Achtung!", draw)
            draw.text((8, title_height), "Karte ist", fill="white")
            draw.text((8, title_height + 8), user["name"], fill="white")
            draw.text((8, title_height + 16), "zugeordnet", fill="white")
            draw.text((8, title_height + 24), "zuerst " + user["name"], fill="white")
            draw.text((8, title_height + 32), "entfernen", fill="white")
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    # erase card
    myReader = SimpleMFRC522.SimpleMFRC522()
    myReader.write(empty_card)

    # wait for user input
    with canvas(device) as draw:
        display_title("Karte Formatieren", draw)
        draw.text((8, title_height), "Karte formatiert", fill="white")

    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def delete_account():
    with canvas(device) as draw:
        display_title("Benutzer entfernen", draw)
        draw.text((8, title_height), "Karte bitte", fill="white")

    action, user_id = read_id()
    if action is not None:
        return action

    # check if user exists do not delete
    user = piorist.get_piorist(user_id)
    if user is not None:
        if user["balance"] > 0.1:
            with canvas(device) as draw:
                display_title("Benutzer entfernen", draw)
                draw.text((8, title_height), "Kontostand von", fill="white")
                draw.text((8, title_height + 8), user["vulgo"]+ " ist", fill="white")
                draw.text((8, title_height + 16), "nicht 0 Fr.", fill="white")
                draw.text((8, title_height + 24), "zuerst leeren", fill="white")

            # wait for user input
            while True:
                if button_back.pressed():
                    return "back"
                if button_pio.pressed():
                    return "pio"
                if button_ok.pressed():
                    return "back"
        else:
            # erase card
            myReader = SimpleMFRC522.SimpleMFRC522()
            myReader.write(empty_card)

            # remove user
            with canvas(device) as draw:
                display_title("Benutzer entfernt", draw)
                draw.text((8, title_height), user["vulgo"], fill="white")
                draw.text((8, title_height + 8), "wurde entfernt", fill="white")
                draw.text((8, title_height + 16), "Karte formatiert", fill="white")
            piorist.delete_piorist(user_id)

            # wait for user input
            while True:
                if button_back.pressed():
                    return "back"
                if button_pio.pressed():
                    return "pio"
                if button_ok.pressed():
                    return "back"
    else:
        with canvas(device) as draw:
            display_title("Benutzer entfernen", draw)
            draw.text((8, title_height), "Benutzer nicht", fill="white")
            draw.text((8, title_height + 8), "gefunden. Karte", fill="white")
            draw.text((8, title_height + 16), "manuell formatieren", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"


def info():
    with canvas(device) as draw:
        display_title("Info", draw)
        draw.text((8, title_height), "Karte bitte", fill="white")

    # setup reader
    myReader = SimpleMFRC522.SimpleMFRC522()

    # read until id got or cancelled
    id, read_id = myReader.read_no_block()
    while not id:
        id, read_id = myReader.read_no_block()
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"

    print(read_id)

    # check whether id is valid
    try:
        user_id=int(read_id)
    except:
        user_id=0

    # gets user data
    user = piorist.get_piorist(user_id)
    if user is not None:
        with canvas(device) as draw:
            display_title("Info", draw)
            draw.text((8, title_height), "Vulgo: " + user["vulgo"], fill="white")
            draw.text((8, title_height+8), "Name: " + user["name"], fill="white")
            draw.text((8, title_height+16), "Kontostand: " + str(user["balance"]/100.0) + " Fr.", fill="white")
            draw.text((8, title_height+24), "Statistik: " + str(user["statistic"]) + " Pio", fill="white")
            draw.text((8, title_height+32), "Abendsstatistik: " + str(user["today"]) + " Pio", fill="white")

    else:
        with canvas(device) as draw:
            display_title("Info", draw)
            draw.text((8, title_height), "Benutzer nicht", fill="white")
            draw.text((8, title_height + 8), "gefunden", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def send_money():
    with canvas(device) as draw:
        display_title("Geld senden", draw)
        draw.text((8, title_height), "Sender", fill="white")
        draw.text((8, title_height + 8), "Karte bitte", fill="white")

    # setup reader
    myReader = SimpleMFRC522.SimpleMFRC522()

    # read until id got or cancelled
    id, read_id = myReader.read_no_block()
    while not id:
        id, read_id = myReader.read_no_block()
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"

    print(read_id)

    # check whether id is valid
    try:
        user_id=int(read_id)
    except:
        user_id=0

    # gets user data
    user = piorist.get_piorist(user_id)

    # check if master
    if read_id == master_id:
        user = {"name":"Master","vulgo":"Master","balance":10000,"card_id":master_id,"statistic":13154,"today":126}

    money_send = 0
    changed_send = True

    if user is not None:
        while True:
            if button_down.pressed():
                money_send -= 100
                changed_send = True
                if money_send < 0:
                    money_send = 0

            if button_up.pressed():
                money_send += 100
                changed_send = True
                if money_send > user["balance"]:
                    money_send = user["balance"]

            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                break

            if changed_send:
                changed_send = False
                with canvas(device) as draw:
                    display_title("Geld senden", draw)
                    draw.text((8, title_height), user["vulgo"], fill="white")
                    draw.text((8, title_height + 8), "Kontostand: " + str(user["balance"]/100.0) + " Fr.", fill="white")
                    draw.text((8, title_height + 16), "senden: " + str(money_send/100.0) + " Fr.", fill="white")
    else:
        with canvas(device) as draw:
            display_title("Geld senden", draw)
            draw.text((8, title_height), "Benutzer nicht", fill="white")
            draw.text((8, title_height + 8), "gefunden", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    with canvas(device) as draw:
        display_title("Geld senden", draw)
        draw.text((8, title_height), "Senden an:", fill="white")
        draw.text((8, title_height + 8), "Karte bitte", fill="white")

    # setup reader
    myReader = SimpleMFRC522.SimpleMFRC522()

    # read until id got or cancelled
    id, read_id = myReader.read_no_block()
    while not id:
        id, read_id = myReader.read_no_block()
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"

    print(read_id)

    # check whether id is valid
    try:
        user_id = int(read_id)
    except:
        user_id = 0

    # gets user data
    user2 = piorist.get_piorist(user_id)

    if user2 is None:
        with canvas(device) as draw:
            display_title("Geld senden", draw)
            draw.text((8, title_height), "Benutzer nicht", fill="white")
            draw.text((8, title_height + 8), "gefunden", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    with canvas(device) as draw:
        display_title("Geld senden", draw)
        draw.text((8, title_height), "Von " + user["vulgo"], fill="white")
        draw.text((8, title_height + 8), str(money_send / 100.0) + " Fr.", fill="white")
        draw.text((8, title_height + 16), "an "+ user2["vulgo"], fill="white")
        draw.text((8, title_height + 24), "senden?", fill="white")

    # wait for confirmation
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with canvas(device) as draw:
        display_title("Geld senden", draw)
        draw.text((8, title_height), "Von " + user["vulgo"], fill="white")
        draw.text((8, title_height + 8), str(money_send / 100.0) + " Fr.", fill="white")
        draw.text((8, title_height + 16), "an "+ user2["vulgo"], fill="white")
        draw.text((8, title_height + 24), "gesendet", fill="white")

    # update balance
    if not user["card_id"] == master_id:
        user["balance"] -= money_send
        piorist.set_piorist(user)

    user2["balance"] += money_send
    piorist.set_piorist(user2)

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def settings_exit():
    with canvas(device) as draw:
        display_title("Beenden", draw)
        draw.text((8, title_height), "wirklich beenden?", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    # do backup
    backup()

    # say pussys von p to y
    with canvas(device) as draw:
        display_title("Beenden", draw)
        draw.text((8, title_height), "Pussys vom", fill="white")
        draw.text((8, title_height + 8), "P bis zum Y", fill="white")

    GPIO.cleanup()
    exit()


def new_connection():
    try:
        request = requests.get('http://people.ee.ethz.ch/~zarron/wlanAPI.php')
    except:
        with canvas(device) as draw:
            display_title("Neue Verbindung", draw)
            draw.text((8, title_height), "Keine Verbindung", fill="white")

        # wait for user input
        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    connection_data = json.loads(request.text)
    with canvas(device) as draw:
        display_title("Neue Verbindung", draw)
        draw.text((8, title_height), "SSID: " + connection_data["ssid"], fill="white")
        draw.text((8, title_height + 8), "Passwort: " + connection_data["passwort"], fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with open("wlan.pio", "r") as file_read:
        wlans = json.load(file_read)
    for wlan in wlans:
        if wlan["ssid"] == connection_data["ssid"]:
            wlans.remove(wlan)

    wlans.append({"ssid":connection_data["ssid"], "passwort":connection_data["passwort"]})

    with open("wlan.pio", "w") as file_write:
        json.dump(wlans,file_write)

    with codecs.open("/etc/wpa_supplicant/wpa_supplicant.conf", "w", "utf-8") as file_write:
        file_write.write("country=CH\nctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\nupdate_config=1\n")
        for wlan in wlans:
            file_write.write("network={\n   ssid=\"" + wlan["ssid"] + "\"\n   psk=\"" + wlan["passwort"] + "\"\n    key_mgmt=WPA-PSK\n    id_str=\"" + wlan["ssid"] + "\"\n}\n")

    with canvas(device) as draw:
        display_title("Neue Verbindung", draw)
        draw.text((8, title_height), "Verbindung", fill="white")
        draw.text((8, title_height + 8), "gespeichert", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def record():
    vulgo = "Niemand"
    pios = 0
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["statistic"]) > pios:
            pios = piorist["statistic"]
            vulgo = piorist["vulgo"]

    with canvas(device) as draw:
        display_title("Rekord", draw)
        draw.text((8, title_height), vulgo, fill="white")
        draw.text((8, title_height + 8), "hat mit " + str(pios) + " Pio", fill="white")
        draw.text((8, title_height + 16), "den Rekord", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def new_day():

    with canvas(device) as draw:
        display_title("Neuer Abend", draw)
        draw.text((8, title_height), "Abend Statistiken", fill="white")
        draw.text((8, title_height + 8), "auf 0 setzen?", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        piorist["today"] = 0
    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    with canvas(device) as draw:
        display_title("Neuer Abend", draw)
        draw.text((8, title_height), "Abend Statistiken", fill="white")
        draw.text((8, title_height + 8), "auf 0 gesetzt", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def welcome_new_day():

    with canvas(device) as draw:
        display_title("Willkommen", draw)
        draw.text((8, title_height), "Neuer Abend", fill="white")
        draw.text((8, title_height + 8), "beginnen?", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with canvas(device) as draw:
        display_title("Neuer Abend", draw)
        draw.text((8, title_height), "Abend Statistiken", fill="white")
        draw.text((8, title_height + 8), "auf 0 setzen?", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            break

    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        piorist["today"] = 0
    with open("list.pio", "w") as write_file:
        json.dump(piorists,write_file)

    with canvas(device) as draw:
        display_title("Neuer Abend", draw)
        draw.text((8, title_height), "Abend Statistiken", fill="white")
        draw.text((8, title_height + 8), "auf 0 gesetzt", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def today_record():
    vulgo = "Niemand"
    pios = 0
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)
    for piorist in piorists:
        if int(piorist["today"]) > pios:
            pios = piorist["today"]
            vulgo = piorist["vulgo"]

    with canvas(device) as draw:
        display_title("Abendsrekord", draw)
        draw.text((8, title_height), vulgo, fill="white")
        draw.text((8, title_height + 8), "hat mit " + str(pios) + " Pio", fill="white")
        draw.text((8, title_height + 16), "den Abendsrekord", fill="white")

    # wait for user input
    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


def statistic_online():
    url = "http://people.ee.ethz.ch/~zarron/send_statistic.php"

    # load passwort
    with open("password.json", "r") as read_file:
        password = json.load(read_file)[0]

    # load data for statistic
    with open("list.pio", "r") as read_file:
        piorists = json.load(read_file)

    vulgo = []
    statistic = []
    today = []

    for piorist in piorists:
        vulgo.append(piorist["vulgo"])
        statistic.append(piorist["statistic"])
        today.append(piorist["today"])

    data = {"vulgo": vulgo, "statistic": statistic, "today": today}

    # generate authentication token
    auth = ""
    for i in range(0, 4):
        auth += random.choice(string.ascii_uppercase + string.digits)

    print(auth)

    payload = {"password": password, "auth": auth, "data": json.dumps(data)}

    # send data
    try:
        r = requests.post(url, data=payload)
        print(r.text)
    except:
        print("keine Verbindung")
        with canvas(device) as draw:
            display_title("Online Statistik", draw)
            draw.text((8, title_height), "keine Verbindung", fill="white")

        while True:
            if button_back.pressed():
                return "back"
            if button_pio.pressed():
                return "pio"
            if button_ok.pressed():
                return "back"

    with canvas(device) as draw:
        display_title("Online Statistik", draw)
        draw.text((8, title_height), "Passwort:", fill="white")
        draw.text((8, title_height + 8), auth, fill="white")

    while True:
        if button_back.pressed():
            return "back"
        if button_pio.pressed():
            return "pio"
        if button_ok.pressed():
            return "back"


# setup RFID-Device
card_reader = SimpleMFRC522.SimpleMFRC522()

# create blank screen
width = 128
height = 64
image = Image.new('1', (width, height))
title_height = 10

# initialize device
serial = spi(device=1, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=24, gpio_RST=25)
device = sh1106(serial, rotate=2)  # sh1106

# empty card
empty_card = "                                                "

# master_id
master_id =  "piopiopiopiopiopiopiopiopiopiopiopiopiopiopiopio"

# pio preis in Rappen
pio_preis = 75

# set GPIO pins
KEY_UP_PIN     = 6
KEY_DOWN_PIN   = 19
OK_PIN         = 21
BACK_PIN       = 20
PIO_PIN        = 16

RED_PIN        = 17
GREEN_PIN      = 27
BUZZER_PIN     = 22

debounce_delay = 200
debounce_delay_buttons = 500

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(OK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(PIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

button_up = GPIO_button.GPIO_button("up", KEY_UP_PIN, debounce_delay)
button_down = GPIO_button.GPIO_button("down", KEY_DOWN_PIN, debounce_delay)
button_ok = GPIO_button.GPIO_button("ok", OK_PIN, debounce_delay_buttons)
button_back = GPIO_button.GPIO_button("back", BACK_PIN, debounce_delay_buttons)
button_pio = GPIO_button.GPIO_button("pio", PIO_PIN, debounce_delay_buttons)

# load all menus
# menus = {"name":{dictionary of one menu}}
menus = {}
menu_list = []
with open("Menus/list.menu","r") as list_file:
    menu_list = json.load(list_file)
    for menu_name in menu_list:
        with open("Menus/" + menu_name + ".json", "r") as menu_file:
            menu_dict = json.load(menu_file)
            menus[menu_dict["name"]] = Menu.Menu(menu_dict)

try:
    with canvas(device) as draw:
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "Willkommen zum", fill="white")
        draw.text((0, 8), "Pio-o-Mat", fill="white")
except:
    print("except")
time.sleep(1)

# enter main menu
selection = 0
current_menu = "welcome_new_day"
draw_menu(device, menus[current_menu], selection)
changed = True

while True:


    if button_down.pressed():
        if len(menus[current_menu].sub)-1 > selection:
            selection += 1
            changed = True
            print("down")

    if button_up.pressed():
        if 0 < selection:
            selection -= 1
            changed = True
            print("up")

    if button_ok.pressed():
        print("ok -> " + menus[current_menu].sub[selection])
        current_menu = menus[current_menu].sub[selection]
        changed = True
        selection = 0

    if button_back.pressed():
            print("back -> " + menus[current_menu].back)
            current_menu = menus[current_menu].back
            changed = True
            selection = 0

    if button_pio.pressed():
            current_menu = "pio"
            changed = True
            print("ok -> pio")
            selection = 0

    if changed:
        changed = False
        if len(menus[current_menu].sub) != 0: # if there are any submenus, display menu screen, otherwise call function
            if draw_menu(device, menus[current_menu], selection):
                break
        else:
            response = globals()[menus[current_menu].function]()
            if response == "pio":
                current_menu = "pio"
                changed = True
                print("? -> pio")
                selection = 0
            elif response == "back":
                print("back -> " + menus[current_menu].back)
                current_menu = menus[current_menu].back
                changed = True
                selection = 0
            else:
                print("no valid response")
                current_menu = "main"
                changed = True
                selection = 0

GPIO.cleanup()
