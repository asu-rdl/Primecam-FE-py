import serial
import serial.tools.list_ports as list_ports
import os, platform, time

cwd = os.path.abspath(os.path.curdir)
print("Current working dir:\n\t", cwd)
cpu = platform.processor()
binfile = cwd+"/build/arduino.samd.nano_33_iot/primecamfe_prototype.ino.bin"

if cpu == "x86_64":
    print("Selecing x64-bossac executable")
    bossac = cwd+"/x64-bossac"
elif cpu == "aarch64":
    print("Selecing aarch64-bossac executable")
    bossac = cwd+"/aarch64-bossac"
else:
    raise Exception("Unknown processor type, expecting x86_64 or aarch64(for the rfsoc)")

if os.path.exists(binfile):
    print("Found arduino firmware bin file")
else:
    raise Exception(f"Compiled arduino bin file not found; \n\tpath={binfile}")


if not os.path.exists(bossac):
    raise Exception(f"bossac executable not found; \n\tpath={bossac}")

# enumerate serial ports looking for the arudino, set it to bootloader mode
def findarduino():
    ports = list_ports.comports()
    possibleports = []
    for p in ports:
        if p.manufacturer == "Arduino LLC":
            possibleports.append(p.device)
    if len(possibleports) > 1:
        raise Exception("Ensure only one arduino is connected to the system")
    elif len(possibleports) == 0:
        return ""
    return possibleports[0]

a = findarduino()
if a == "":
    raise Exception("Couldn't locate arduino")
    
print(f"Found arduino at {a}, Performing 1200-bps touch reset on serial port /dev/ttyACM0")
s = serial.Serial(a, baudrate=1200)
s.close()
print("waiting for arduino port")
time.sleep(2)

a = findarduino()

if a == "":
    raise Exception("Couldn't locate arduino")

print(f"Found arduino at {a}")

# Upload firmware
args = f' -i -d --port={a.replace("/dev/", "")} -U true -i -e -w -v "{binfile}" -R'
os.system(bossac+args)
print("done.")