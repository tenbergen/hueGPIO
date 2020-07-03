import RPi.GPIO as GPIO
import time

# PIN Setup -- set this to whatever pin you have the LED hooked up to
pin_id = 2

# GPIO Infrastructure for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_id, GPIO.OUT)
GPIO.output(pin_id, GPIO.LOW)


# blink at startup so we know you're ready
def blink():
    for n in range(10):
        GPIO.output(pin_id, GPIO.HIGH)
        time.sleep(0.25)
        GPIO.output(pin_id, GPIO.LOW)
        time.sleep(0.25)


# Interface function to allow hueGPIO to control on/off state
def setHueColor(color, bright):
    if bright == 0.0:
        GPIO.output(pin_id, GPIO.LOW)
    else:
        GPIO.output(pin_id, GPIO.HIGH)


blink()
# END.
