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

# setup RFID-Device
card_reader = SimpleMFRC522.SimpleMFRC522()

# create blank screen
width = 128
height = 64
image = Image.new('1', (width, height))

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

# load all Menus


try:
    with canvas(device) as draw:
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "Willkommen zum", fill="white")
        draw.text((0, 8), "Pio-o-Mat", fill="white")
        draw.text((0, 24), "Press OK for Menu", fill="white")
        draw.text((0, 32), "Press Pio for Pio", fill="white")
        time.sleep(1)
        draw.rectangle([(0,0),(128,64)], fill="black")
except:
    print("except")

GPIO.cleanup()
