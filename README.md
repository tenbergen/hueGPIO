# hueGPIO
A Raspberry Pi middleware for diyHUE to control LEDs connected to GPIO

## Requirements
- Raspberry Pi (tested with 3b+, 4, ZeroW)
- some LEDs wired up to GPIO (google how.)
- diyHUE installed (either on this Raspberr Pi or somewhere else):<br>
  https://diyhue.readthedocs.io/en/latest/getting_started.html#automatic-install 

## Software Dependencies
- Raspbian Stretch or higher
- python3 with pip3 and flask
<p>Other libraries or python modules may be required, e.g. for adafruit neopixels. Install them separately.</p>

## Installation
In a terminal, execute:
```
git clone https://github.com/tenbergen/hueGPIO.git
cd hueGPIO
sudo -s
sh install.sh
```
The service will start immediately and after reboot.
<p>Other libraries or python modules may be required, e.g. for adafruit neopixels. Install them separately.</p>

### Adding your own lights
hueGPIO will be default run an emulated light.<br>
To add your own GPIO LEDs or neopixels, first wire them up correctly like you normally would.<br>
Then:
1. Open `http://{diyHUE-IP-address}/milight` in your browser
2. Under `Hub ip`, add the IP address of where your have hueGPIO installed, followed by ":5000", as the port is 5000.<br>
This can be the same Raspberry Pi as the one running diyHUE, in which case, you can simple enter `127.0.0.1:5000` or `localhost:5000`
3. Under `Device id`, enter a number in the form `0x1234`
4. Under `Mode`, select `RGB`
5. Under `Group`, select `1`
6. Click `Save`
<p>
Next, edit `hueGPIO.py` as follows:
</p>

- In line 3 of the file, change
```python
from gpio_lights import light_emulator
```
to something else, e.g., 
```python
from gpio_lights import neopixel
```
It might be a module available in the folder `gpio_lights`, however.
- Locate the 20 lines at the end of the file starting with `#SNIP` and ending with `#SNAP`"
```python
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
``` 
- Copy and paste everything in between
- Modify every occurrence of the number `0x0001` to the same number that you entered under Step 3 in diyHUE, e.g., `0x1234`. This should only be in the first three lines after `#SNIP`:
```python
@app.route('/gateways/0x1234/rgb/1', methods=['PUT', 'GET'])
def light_0x1234():
    name = "0x1234"
```
- In the code you just pasted, change the line
```python
light_emulator.setHueColor(...)
```
to the same that you have selected in line 3 of the file.
- Repeat these steps for any additional light.

### Control the service
After adding your own light, you may need to restart the service via command line. Run:
```
sudo systemctl restart hueGPIO.service
```

## Extending hueGPIO
In principle, any GPIO device can be controlled using hueGPIO, as long as it contains a method
`setHueColor((red, green, blue), brightness)`.<br>
<br>
Reading from GPIO devices is currently not supported.

## Limitations
Share the love and improve this thing:
- Flask internal development server is used, which is unsafe. Upgrade to production server.
- Add support for other GPIO devices.
- Add support for reading from GPIO devices.
- LEDs don't turn off when hueGPIO is killed.

## See also
[neocal](https://github.com/tenbergen/neocal)  - A perpetual calendar for Raspberry Pi using NeoPixel LED lights.<br>
[neotemp](https://github.com/tenbergen/neotemp) - An adafruit NeoPixel stick thermostat for Raspberry Pi.