import atexit
import RPi.GPIO as GPIO
import time

# PIN Setup -- set this to whatever pins you have the LED hooked up to
red_pin   = 20
green_pin = 21
blue_pin  = 22
min       = 0 #start PWM at 0% duty cycle
max       = 100 #maximum durty cycle

# GPIO Infrastructure for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)
r = GPIO.PWM(red_pin, max)
g = GPIO.PWM(green_pin, max)
b = GPIO.PWM(blue_pin, max)
r.start(min)
g.start(min)
b.start(min)


# pulse at startup so we know you're ready
def cycle():
    for x in range(min, max):
        r.ChangeDutyCycle(x)
        time.sleep(0.005)
    for x in range(min, max):
        g.ChangeDutyCycle(x)
        r.ChangeDutyCycle(max - x)
        time.sleep(0.005)
    for x in range(min, max):
        b.ChangeDutyCycle(x)
        g.ChangeDutyCycle(max - x)
        time.sleep(0.005)
    for x in range(min, max):
        r.ChangeDutyCycle(x)
        b.ChangeDutyCycle(max - x)
        time.sleep(0.005)
    r.ChangeDutyCycle(min)
    g.ChangeDutyCycle(min)
    b.ChangeDutyCycle(min)

# Interrupt handler that turns LED and releases hardware lock when the program exits (SIGTERM).
def interrupt():
    r.ChangeDutyCycle(min)
    r.stop()
    g.ChangeDutyCycle(min)
    g.stop()
    b.ChangeDutyCycle(min)
    b.stop()
    GPIO.cleanup()

# Interface function to allow hueGPIO to control PWM signal on led pins
def setHueColor(color, bright):
    print("color: ", color, "bright: ", bright)
    red, green, blue = color
    #adjust brightness
    red = red * bright
    green = green * bright
    blue = blue * bright
    #convert color from 0..255 RGB interval to 0..100 PWM signal
    red = int(round((100 / 255 * red), 0))
    green = int(round((100 / 255 * green), 0))
    blue = int(round((100 / 255 * blue), 0))
    r.ChangeDutyCycle(red)
    g.ChangeDutyCycle(green)
    b.ChangeDutyCycle(blue)


atexit.register(interrupt)
cycle()
# END.

