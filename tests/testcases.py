import unittest
from  primecamfe import Primecamfe

"""
Code assumes:
 the microcontroller is connected, programmed, and on.
 the system is linux
 the operating system assigned the device to the path /dev/ttyACM0
"""

class FunctionalTestSet(unittest.TestCase):

    def test_real_connection(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        self.assertTrue(attenobj.connected)

    def test_set_all_to_zero(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        for i in range(0,7+1):
            a,b = attenobj.set_atten(i, 0)
            self.assertTrue(a)
            print(f"Test Channel {i}, {"PASS" if a else "FAIL"}")

    def test_set_all_to_max(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        for i in range(0,7+1):
            a,b = attenobj.set_atten(i, 31.75)
            self.assertTrue(a)
            print(f"Test Channel {i}, {"PASS" if a else ""}")

class InvalidInputTestSet(unittest.TestCase):

    def test_port_not_found(self):
        with self.assertRaises(ConnectionError):
            attenobj = Primecamfe("PORTYPORTTHATISNTREAL")

    def test_bad_atten(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        with self.assertRaises(AssertionError):
            a, b = attenobj.set_atten(0, 50)
            self.assertFalse(a)
            print(b)

    def test_bad_addr(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        with self.assertRaises(AssertionError):
            a, b = attenobj.set_atten(9, 0)

        with self.assertRaises(AssertionError):
            a, b = attenobj.set_atten(-1, 0)




if __name__ == '__main__':
    unittest.main()