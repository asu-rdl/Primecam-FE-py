import serial.tools.list_ports
import time
import struct

_ASSERTIONS = True
_ENABLE_DEBUG = False


class Primecamfe:
    def __init__(self, comport) -> None:
        self.ser = serial.Serial(comport, baudrate=115200, timeout=5)
        time.sleep(.250)
        if self.ser.is_open:
            self.ser.write(b"get_id\n")
            resp = self.ser.read_until(b"\n")
            if resp.strip() == b"primecam_amp_frontend":
                print("Connected")
            else:
                self.ser.close()
                raise ConnectionError("Primecam RF Frontend Amp Controller didn't respond as expected to an id query")
        else:
            raise ConnectionError("Couldn't open serial port.")
        
    
    def set_atten(self, addr:int, value : float):
        if not self.ser.is_open:
            raise ConnectionError("Not connected to Primecam RF Frontend Amp Controller")
        if _ASSERTIONS:
            assert value >= 0 and value <= 31.75, "Attenuation out of range (0 through 31.75)"
            assert addr >= 1 and addr <= 8, "Address out of range (1 through 8)"
        atten = int(round(value*4))&0xFF
        address = addr&0xFF
        data = struct.pack('<BB', address, atten)
        self.ser.write(b"set_atten\n")
        self.ser.write(data)
        response = self.ser.read_until(b'\n')
        if response.strip() == b'OK':
            if _ENABLE_DEBUG:
                return True, "OK", atten
            else:
                return True, "OK"
        else:
            msg = response.decode().strip('\n').strip('\r')
            if len(msg) == 0:
                print("Error, device did not respond")
            else:
                return False, msg

    def __del__(self):
        if self.ser.is_open:
            self.ser.close()

    def close(self):
        if self.ser.is_open:
            self.ser.close()

    def open(self):
        if not self.ser.is_open:
            self.ser.open()

