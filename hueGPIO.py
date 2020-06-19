import atexit, math, json, os.path
from flask import Flask, request, jsonify
from gpio_lights import light_emulator

# FLASK INFRASTRUCTURE
path = '/home/pi/hueGPIO/'
app = Flask(__name__)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


@app.route('/')
def index():
    return "hueGPIO - a middleware to translate diyHUE JSON requests to generic Raspberry Pi GPIO commands."


# HELPER METHODS
# Converts brightness from 0..255 interval to 0..1 interval.
def convertbrightness(requestedbrightness):
    return round((1.0 / 255 * requestedbrightness), 4)

# Converts the color temperature from 153..370 mireds to 1000..40000 K for RGB conversion.
# Milights' color temperature is measured in mireds (https://sidoh.github.io/esp8266_milight_hub/branches/latest/#tag/Device-Control/paths/~1gateways~1{device-id}~1{remote-type}~1{group-id}/put)
# but diyHUE sends values all the way to to 463. This will undoubtedly cause cause the color temperature to be inaccurate.
def converttemperature(requestedtemperature):
    return ((requestedtemperature - 153) / (460 - 153)) * (40000 - 1000) + 1000

# Converts color temperature to RGB.
# from: https://gist.github.com/petrklus/b1f427accdf7438606a6
def convert_K_to_RGB(colour_temperature):
    """
    Converts from K to RGB, algorithm courtesy of
    http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
    """
    # range check
    if colour_temperature < 1000:
        colour_temperature = 1000
    elif colour_temperature > 40000:
        colour_temperature = 40000

    tmp_internal = colour_temperature / 100.0

    # red
    if tmp_internal <= 66:
        red = 255
    else:
        tmp_red = 329.698727446 * math.pow(tmp_internal - 60, -0.1332047592)
        if tmp_red < 0:
            red = 0
        elif tmp_red > 255:
            red = 255
        else:
            red = tmp_red

    # green
    if tmp_internal <= 66:
        tmp_green = 99.4708025861 * math.log(tmp_internal) - 161.1195681661
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green
    else:
        tmp_green = 288.1221695283 * math.pow(tmp_internal - 60, -0.0755148492)
        if tmp_green < 0:
            green = 0
        elif tmp_green > 255:
            green = 255
        else:
            green = tmp_green

    # blue
    if tmp_internal >= 66:
        blue = 255
    elif tmp_internal <= 19:
        blue = 0
    else:
        tmp_blue = 138.5177312231 * math.log(tmp_internal - 10) - 305.0447927307
        if tmp_blue < 0:
            blue = 0
        elif tmp_blue > 255:
            blue = 255
        else:
            blue = tmp_blue

    return red, green, blue


# CUSTOM LIGHT INFRASTRUCTURE
# required to make light states persistent and give feedback to Hue app.
class LightState:
    def __init__(self, name):
        self.state = False
        self.status = False
        self.hue = 0
        self.saturation = 0
        self.kelvin = 0
        self.temperature = 0
        self.color_temp = 0
        self.mode = 0
        self.red = 255
        self.green = 255
        self.blue = 255
        self.level = 0
        self.brightness = 0.5
        self.effect = "night_mode"
        self.transition = 2
        self.name = name

    def save(self, filename):
        with open(filename, 'w') as outfile:
            json.dump(self.serialize(), outfile)

    def load(self, filename):
        with open(filename) as json_file:
            data = json.load(json_file)
            self.state = data['state']
            self.status = data['status']
            self.hue = data['hue']
            self.saturation = data['saturation']
            self.kelvin = data['kelvin']
            self.temperature = data['temperature']
            self.color_temp = data['color_temp']
            self.mode = data['mode']
            rgb = data['color'].split(',')
            self.red = rgb[0]
            self.green = rgb[1]
            self.blue = rgb[2]
            self.level = data['level']
            self.brightness = data['brightness']
            self.effect = data['effect']
            self.transition = data['transition']
            self.name = data['name']

    def serialize(self):
        return {
            'state': self.state,
            'status': self.status,
            'hue': self.hue,
            'saturation': self.saturation,
            'kelvin': self.kelvin,
            'temperature': self.temperature,
            'color_temp': self.color_temp,
            'mode': self.mode,
            'color': str(self.red) + ',' + str(self.green) + ',' + str(self.blue),
            'level': self.level,
            'brightness': self.brightness,
            'effect': self.effect,
            'transition': self.transition,
            'name': self.name
        }


# Parses the JSON request sent by diyHUE.
def parserequest(requestjson, currentstate):
    parsedstate = currentstate

    if 'status' in requestjson:
        parsedstate.status = requestjson['status']
        parsedstate.state = parsedstate.state
        if parsedstate.status:
            parsedstate.brightness = 1.0
        else:
            parsedstate.brightness = 0.0
    if 'fill' in requestjson:
        print("Unknown command: fill.", requestjson['fill'])
    if 'brightness' in requestjson:
        parsedstate.brightness = convertbrightness(requestjson['brightness'])
    if 'color' in requestjson:
        parsedstate.red = requestjson['color']['r']
        parsedstate.green = requestjson['color']['g']
        parsedstate.blue = requestjson['color']['b']
    if 'color_temp' in requestjson:
        (r, g, b) = convert_K_to_RGB(converttemperature(requestjson['color_temp']))
        parsedstate.red = int(math.floor(r))
        parsedstate.green = int(math.floor(r))
        parsedstate.blue = int(math.floor(r))

    return parsedstate


# METHODS FOR CUSTOM LIGHTS
# COPY THE METHOD AND CHANGE 0x0001 to something else for each additional light.
#SNIP
@app.route('/gateways/0x0001/rgb/1', methods=['PUT', 'GET'])
def light_0x0001():
    name = "0x0001"

    if not request.is_json:
        return 'Please add this light to diyHUE: <a href="https://diyhue.readthedocs.io/en/latest/lights/milight.html">https://diyhue.readthedocs.io/en/latest/lights/milight.html</a>'

    lightstate = LightState(name)
    filename = path + str(name) + '.json'
    if os.path.isfile(filename):
        lightstate.load(filename)

    changedstate = parserequest(request.get_json(), lightstate)
    changedstate.name = name
    changedstate.save(filename)

    light_emulator.setHueColor((changedstate.red, changedstate.green, changedstate.blue), changedstate.brightness)

    return jsonify(changedstate.serialize())
# SNAP
