import time
import RPi.GPIO as GPIO

current_milli_time = lambda: int(round(time.time() * 1000))


class GPIO_button:
    def __init__(self, name, pin, debounce_delay):
        self.name = name
        self.pin = pin
        self.debounce_delay = debounce_delay
        self.debounce_time = current_milli_time()

    def pressed(self):
        if not GPIO.input(self.pin):
            if current_milli_time() > self.debounce_time + self.debounce_delay:
                self.debounce_time = current_milli_time()
                return True
        return False