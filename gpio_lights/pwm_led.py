import atexit
import RPi.GPIO as GPIO
import time

# PIN Setup -- set this to whatever pin you have the LED hooked up to
pin_id = 21
min    = 0 #start PWM at 0% duty cycle
max    = 100 #maximum durty cycle

# GPIO Infrastructure for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin_id, GPIO.OUT)
pwm = GPIO.PWM(pin_id, max)
pwm.start(min)


# pulse at startup so we know you're ready
def pulse():
    for x in range(max):
        pwm.ChangeDutyCycle(x)
        time.sleep(0.01)

    for x in reversed(range(max)):
        pwm.ChangeDutyCycle(x)
        time.sleep(0.01)


# Interrupt handler that turns LED and releases hardware lock when the program exits (SIGTERM).
def interrupt():
    pwm.ChangeDutyCycle(min)
    pwm.stop()
    GPIO.cleanup()


# Interface function to allow hueGPIO to control brightness
def setHueColor(color, bright):
    bright = int(round(100 * bright, 0))
    pwm.ChangeDutyCycle(bright)


atexit.register(interrupt)
pulse()
# END.

