import unittest
from  primecamfe import Primecamfe

class Test_serial_connection(unittest.TestCase):
    def test_port_not_found(self):
        with self.assertRaises(ConnectionError):
            attenobj = Primecamfe("PORTYPORTTHATISNTREAL")

    def test_real_connection(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        self.assertTrue(attenobj.connected)


if __name__ == '__main__':
    unittest.main()