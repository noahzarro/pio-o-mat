import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

print("Deborah ist wunderschön")
print("LED on")

for i in range(0,99):
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)
    time.sleep(0.2)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(18, GPIO.LOW)
    time.sleep(0.2)


print("LED off")
GPIO.cleanup()