# Primecam-FE-py
RFSoC Frontend Amp Board Attenuator Controls

Note: After a full power cycle of the attenuators where they have never been commanded, get_atten will return 63.75 which is invalid. They nevertheless start in a max attenuation state of 31.75 dB.

# Installation
____
* Open a terminal and run pip
  * `pip install https://github.com/asu-rdl/Primecam-FE-py/releases/latest/download/primecamfe-0.1.1-py3-none-any.whl`
* Or visit github and download the whl file from here and install manually:
  * https://github.com/asu-rdl/Primecam-FE-py/releases/latest
  * `pip install ./primecamfe-X.X.X-py3-none-any.whl`
* If installing on an RFSoC with no internet, you'll want to download [pyserial](https://pypi.org/project/pyserial/#files)
and install both together.
  * `pip install ./primecamfe-X.X.X-py3-none-any.whl ./pyserial-3.5-py2.py3-none-any.whl`

    
# Usage
_______
The channels are numbered 0 through 7.


***class*** *Primecamfe*:
```
Primecam RF Front End control. On initialization this will attempt to connect
to the provided device and verify it works with this software
```
**Parameters** 
```
comport : str
        Comport or path that the attenuator is connected to.
        eg: COM13 or /dev/ttyACM0  (users can create permanent simlinks to this dev using udevrules in Ubuntu)
```
**Methods**
```
set_atten(addr, value):
    Sets the attenuator to the provided value.
    addr : int
        Channel or address of the attenuator  (0 through 7)
    value: float 
        Value of the attenuator (0 through 31.75)
    return : bool
     returns True if success/False otherwise.

    If _ENABLE_DEBUG is asserted then a tuple is returned

get_atten(addr):
    Returns the attenuator value at the provided address.
    address : int
        Channel or address of the attenuator  (0 through 7)
    return : float
        The channel's current attenuation setting
```


## Example

```python
from primecamfe import Primecamfe

fe1 = Primecamfe('/dev/ttyUSB0')

# set all the attenuators to 31.75 dB of attenuation
for channel in range(0, 7 + 1):
    fe1.set_atten(channel, 31.75)

# read back the attenuators
for channel in range(0, 7 + 1):
    print(fe1.get_atten(channel))
```

# Updating the Microcontroller Firmware
1. Download and install the latest Arduino IDE
1. In the IDE, under preferences add the following url to the 'Additional boards manager URLs' box
   1. `https://files.seeedstudio.com/arduino/package_seeeduino_boards_index.json`
1. Open the sketch from this repository under mcu_firmware/primecam/primecam.ino
1. Set the board to `Seeeduino XIAO`
1. Press upload. There are no additional libraries required.
1. Verify operation (optionally this library's unit tests)
