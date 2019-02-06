# pio-o-mat, for managing beer consumption at serafins ruemli

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.core import lib

from luma.oled.device import sh1106
import RPi.GPIO as GPIO

import time
import subprocess

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import SimpleMFRC522

import piorist
import Menu

import json

# function definitions

current_milli_time = lambda: int(round(time.time() * 1000))

def draw_menu(device, menu, selection):
    try:
        with canvas(device) as draw:
            # clear everything
            draw.rectangle([(0, 0), (128, 64)], fill="black")
            # draw titlebox
            draw.rectangle([(0, 0), (128, title_height)], fill="white")
            draw.text((1, 1), menu.title, fill="black")
            # draw submenus
            i=0
            for submenu in menu.sub:
                draw.text((8,title_height+i*8),submenu, fill="white")
                i += 1
            # draw selection
            draw.polygon([(1,title_height+selection*8+2),(1,title_height+selection*8+8),(4,title_height+selection*8+5)], fill="white")
            return 0
    except:
        print("except")
        return 1


# setup RFID-Device
card_reader = SimpleMFRC522.SimpleMFRC522()

# create blank screen
width = 128
height = 64
image = Image.new('1', (width, height))
title_height = 10

# initialize device
serial = spi(device=0, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=24, gpio_RST=25)
device = sh1106(serial, rotate=2)  # sh1106

# set GPIO pins
KEY_UP_PIN     = 6
KEY_DOWN_PIN   = 19
OK_PIN       = 21
BACK_PIN       = 20
PIO_PIN       = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Input with pull-up
GPIO.setup(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Input with pull-up
GPIO.setup(OK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(BACK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up
GPIO.setup(PIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)      # Input with pull-up

# load all menus
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
        draw.text((0, 24), "Press OK for Menu", fill="white")
        draw.text((0, 32), "Press Pio for Pio", fill="white")
except:
    print("except")
time.sleep(1)

# enter main menu
selection = 0
current_menu = "main"
draw_menu(device, menus[current_menu], selection)

# set debounce timers

debounce_delay = 200

debounce_up = current_milli_time()
debounce_down = current_milli_time()
debounce_pio = current_milli_time()
debounce_ok = current_milli_time()
debounce_back = current_milli_time()


while True:

    changed = False
    if not GPIO.input(KEY_DOWN_PIN):
        if current_milli_time() > debounce_down + debounce_delay:
            debounce_down = current_milli_time()
            if len(menus[current_menu].sub)-1 > selection:
                selection += 1
                changed = True
                print(selection)

    if not GPIO.input(KEY_UP_PIN):
        if current_milli_time() > debounce_up + debounce_delay:
            debounce_up = current_milli_time()
            if 0 < selection:
                selection -= 1
                changed = True
                print(selection)


    if changed:
        print("iteration")
        if draw_menu(device, menus[current_menu], selection):
            break


GPIO.cleanup()
