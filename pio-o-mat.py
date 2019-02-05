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

# setup RFID-Device
card_reader = SimpleMFRC522.SimpleMFRC522()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))

serial = spi(device=0, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=24, gpio_RST=25)

device = sh1106(serial, rotate=2)  # sh1106

try:
    with canvas(device) as draw:
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "Willkommen zum", fill="white")
        draw.text((0, 8), "Pio-o-Mat", fill="white")
        draw.text((0, 16), "Press OK for Menu", fill="white")
        draw.text((0, 24), "Press Pio for Pio", fill="white")
except:
    print("except")

GPIO.cleanup()
