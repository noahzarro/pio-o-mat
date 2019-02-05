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

# setup reader
myReader = SimpleMFRC522.SimpleMFRC522()
result = myReader.read()


# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = 128
height = 64
image = Image.new('1', (width, height))

serial = spi(device=0, port=0, bus_speed_hz=8000000, transfer_size=4096, gpio_DC=24, gpio_RST=25)

device = sh1106(serial, rotate=2)  # sh1106

print(result)


try:
    with canvas(device) as draw:
        # draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((0, 0), "Suc se cuk", fill="white")
        draw.text((0, 8), "Fagitoli", fill="white")
except:
    print("except")

GPIO.cleanup()

