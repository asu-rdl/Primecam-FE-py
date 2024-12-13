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


# Updating the Microcontroller Firmware Through the RFSoC for the Prototype Board
1. Clone this repository
1. Open a terminal and navigate to `mcu_firmware` within this repository
1. Scp the `primecamfe_prototype` firmware to the RFSoC
    1. `scp -r primecamfe_prototype xilinx@some.ip.address.here:~/
1. ssh into the RFSoC `ssh xilinx@some.ip.address.here`
1. `sudo -s`
1. `source activate.sh` activate the python pynq virtual env, 
    1. if not present then copy & paste from the `RFSoC Python Activation Script` below
    1. `touch activate.sh; chmod +x activate.sh; nano activate.sh` 
    1. paste, save, close, `source activate.sh`
1. `cd primecamfe_prototype`
1. `python FirmwareUpdater.py`
1.  you should see something like the output below


```
(pynq-venv) root@pynq-rfsoc:/home/xilinx/primecamfe_prototype# python FirmwareUpdater.py 
Current working dir:
	 /home/xilinx/primecamfe_prototype
Selecing aarch64-bossac executable
Found arduino firmware bin file
Found arduino at /dev/ttyACM0, Performing 1200-bps touch reset on serial port /dev/ttyACM0
waiting for arduino port
Found arduino at /dev/ttyACM0
Set binary mode
readWord(addr=0)=0x20007ffc
readWord(addr=0xe000ed00)=0x410cc601
readWord(addr=0x41002018)=0x10010305
version()=v2.0 [Arduino:XYZ] Apr 19 2019 14:38:48
chipId=0x10010005
Connected at 921600 baud
readWord(addr=0)=0x20007ffc
readWord(addr=0xe000ed00)=0x410cc601
readWord(addr=0x41002018)=0x10010305
Atmel SMART device 0x10010005 found
write(addr=0x20004000,size=0x34)
writeWord(addr=0x20004030,value=0x10)
writeWord(addr=0x20004020,value=0x20008000)
Device       : ATSAMD21G18A
readWord(addr=0)=0x20007ffc
readWord(addr=0xe000ed00)=0x410cc601
readWord(addr=0x41002018)=0x10010305
Chip ID      : 10010005
version()=v2.0 [Arduino:XYZ] Apr 19 2019 14:38:48
Version      : v2.0 [Arduino:XYZ] Apr 19 2019 14:38:48
Address      : 8192
Pages        : 3968
Page Size    : 64 bytes
Total Size   : 248KB
Planes       : 1
Lock Regions : 16
Locked       : readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
readWord(addr=0x41004020)=0xffff
none
readWord(addr=0x41004018)=0
Security     : false
Boot Flash   : true
readWord(addr=0x40000834)=0x7000a
BOD          : true
readWord(addr=0x40000834)=0x7000a
BOR          : true
Arduino      : FAST_CHIP_ERASE
Arduino      : FAST_MULTI_PAGE_WRITE
Arduino      : CAN_CHECKSUM_MEMORY_BUFFER
Erase flash
chipErase(addr=0x2000)
done in 0.822 seconds

Write 14632 bytes to flash (229 pages)
write(addr=0x20005000,size=0x1000)
writeBuffer(scr_addr=0x20005000, dst_addr=0x2000, size=0x1000)
[========                      ] 27% (64/229 pages)write(addr=0x20005000,size=0x1000)
writeBuffer(scr_addr=0x20005000, dst_addr=0x3000, size=0x1000)
[================              ] 55% (128/229 pages)write(addr=0x20005000,size=0x1000)
writeBuffer(scr_addr=0x20005000, dst_addr=0x4000, size=0x1000)
[=========================     ] 83% (192/229 pages)write(addr=0x20005000,size=0x940)
writeBuffer(scr_addr=0x20005000, dst_addr=0x5000, size=0x940)
[==============================] 100% (229/229 pages)
done in 0.119 seconds

Verify 14632 bytes of flash with checksum.
checksumBuffer(start_addr=0x2000, size=0x1000) = 11d7
checksumBuffer(start_addr=0x3000, size=0x1000) = 44ab
checksumBuffer(start_addr=0x4000, size=0x1000) = cacb
checksumBuffer(start_addr=0x5000, size=0x928) = 2516
Verify successful
done in 0.018 seconds
CPU reset.
readWord(addr=0)=0x20007ffc
readWord(addr=0xe000ed00)=0x410cc601
readWord(addr=0x41002018)=0x10010305
writeWord(addr=0xe000ed0c,value=0x5fa0004)
done.

```




```bash
# RFSoC Python Activation Script
#!/bin/bash

cd /home/xilinx/
# Source the environment as the init system won't
set -a
. /etc/environment
set +a
for f in /etc/profile.d/*.sh; do source $f; done
```
