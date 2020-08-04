import board, neopixel
import atexit, time

# NeoPixel Setup
neopixel_pin = board.D18  # Set to where DATA line is connected.
neopixel_length = 8  # Set to how many lights there are on the NeoPixel strand. 8 = one adafruit NeoPixel stick
brightness = 1.0  # Set how bright in the range [0..1] the NeoPixels shall be.
order = neopixel.GRB  # adafruit NeoPixel stick are (green, red, blue), others may be (red, green, blue)

# Color Setup - adjust colors to your preference.
# Note: The more white they are and the more pixels are lit, the more current it draws,
# so make sure your power supply provides at least 3amps to your pixels.
off = (0, 0, 0)  # used for "inactive" pixels, i.e., pixels that aren't lit
hue_color = off  # used to set the color send by diyHUE via hueGPIO
black = off
white = (255, 255, 255)  # for reference - color tuples are in RGB (red, green, blue)

DEBUG = False
pixels = neopixel.NeoPixel(neopixel_pin, neopixel_length, brightness=brightness, pixel_order=order)

# Interface function to allow hueGPIO to control "hue_color"
def setHueColor(color, bright):
    global hue_color
    global brightness
    hue_color = int(color[0]), int(color[1]), int(color[2])
    brightness = bright
    pixels.brightness = brightness
    pixels.fill(hue_color)


# Interrupt handler that turns pixels off when the program exits (SIGTERM).
def interrupt():
    pixels.fill(off)


# when hueGPIO exits (SIGTERM), turn off pixels.
atexit.register(interrupt)
# END.
