import atexit

# Color Setup - adjust colors to your preference.
# Note: The more white they are and the more pixels are lit, the more current it draws,
# so make sure your power supply provides at least 3amps to your pixels.
off = (0, 0, 0)  # used for "inactive" pixels, i.e., pixels that aren't lit
hue_color = off  # used to set the color send by diyHUE via hueGPIO
black = off
white = (255, 255, 255)  # for reference - color tuples are in RGB (red, green, blue)

# Interface function to allow hueGPIO to control "hue_color"
def setHueColor(color, bright):
    global hue_color
    global brightness
    hue_color = int(color[0]), int(color[1]), int(color[2])
    brightness = bright
    print("New command received from hueGPIO. Color: ", color, "; brightness: ", brightness)


# Interrupt handler that turns pixels off when the program exits (SIGTERM).
def interrupt():
    print("Emulated light. Exiting.")

# when hueGPIO exits (SIGTERM), turn lights off.
atexit.register(interrupt)

print("Emulated light ready.")
# END.
