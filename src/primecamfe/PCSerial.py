
import serial.tools.list_ports
import struct

_ASSERTIONS = True
_ENABLE_DEBUG = False

class Primecamfe:
    def __init__(self, comport) -> None:
        """
        Primecam RF Front End control. On initialization this will attempt to connect
        to the provided device and verify it works with this software
        :param comport: Comport or path that the attenuator is connected to.
            eg: COM13 or /dev/ttyACM0  (users can create permanent simlinks to this dev using udevrules in Ubuntu)
        """
        self.connected = False
        try:
            self.ser = serial.Serial(comport, baudrate=115200, timeout=5)
        except serial.SerialException:
            raise ConnectionError("Serial port doesn't exist")
        if self.ser.is_open:
            self.connected = True
            self.ser.write(b"get_id\n")
            resp = self.ser.read_until(b"\n")
            if resp.strip(b"\r\n ") == b"primecam_amp_frontend":
                print("Connected")
            else:
                self.ser.close()
                raise ConnectionError("Primecam RF Frontend Amp Controller didn't respond as expected to an id query")
        else:
            raise ConnectionError("Couldn't open serial port.")
        
    
    def set_atten(self, addr:int, value : float):
        """
        Sets the attenuator to the provided value.
        :param addr: Channel or address of the attenuator  (0 through 7)
        :param value: Value of the attenuator (0 through 31.75)
        :return: returns bool: True if success/False otherwise.

        If _ENABLE_DEBUG is asserted then a tuple is returned
        """
        if not self.ser.is_open:
            raise ConnectionError("Not connected to Primecam RF Frontend Amp Controller")
        if _ASSERTIONS:
            assert value >= 0 and value <= 31.75, "Attenuation out of range (0 through 31.75)"
            assert addr >= 0 and addr <= 7, "Address out of range (0 through 7)"
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
                return True
        else:
            print(response) if _ENABLE_DEBUG else None
            msg = response.decode().strip('\n').strip('\r')
            if len(msg) == 0:
                print("Error, device did not respond")
            else:
                return (False, msg) if _ENABLE_DEBUG else False


    def get_atten(self, addr:int) -> float:
        """
        Returns the attenuator value at the provided address.
        :param addr: Channel or address of the attenuator  (0 through 7)
        :return: The channel's current attenuation setting
        """
        if not self.ser.is_open:
            raise ConnectionError("Couldn't open serial port.")
        if _ASSERTIONS:
            assert addr >= 0 and addr <= 7, "Address out of range (0 through 7)"
        self.ser.write(b"get_atten\n")
        data = struct.pack('<B', addr)
        self.ser.write(data)
        response = self.ser.readline()
        rrr = response.decode().strip('\n\r')
        try:
            x = int(rrr)
        except ValueError:
            raise ValueError("Unexpected value returned from microcontroller.")
        return x/4.0


    def close(self):
        if self.ser.is_open:
            self.ser.close()

    def open(self):
        if not self.ser.is_open:
            self.ser.open()

