import unittest

from src.primecamfe import Primecamfe

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
            a = attenobj.set_atten(i, 0)
            self.assertTrue(a)
            print(f"Test Channel {i}, {"PASS" if a else "FAIL"}")

    def test_set_all_to_max(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        for i in range(0,7+1):
            a = attenobj.set_atten(i, 31.75)
            self.assertTrue(a)
            print(f"Test Channel {i}, {"PASS" if a else ""}")

    def test_get_atten(self):
        attenobj = Primecamfe("/dev/ttyACM0")
        print(attenobj.get_atten(0))

    def test_get_atten_after_set(self):
        from src.primecamfe import PCSerial
        PCSerial._ENABLE_DEBUG = True
        attenobj = Primecamfe("/dev/ttyACM0")
        for j in range(0, 7+1):
            for i in range(0, 31):
                print(f"Test Channel {j}, Attenuation {i}")
                attenobj.set_atten(j, i)
                a = attenobj.get_atten(j)
                self.assertEqual(a, i)
                print("PASS")
        PCSerial._ENABLE_DEBUG = False

    def test_rounding(self):
        from src.primecamfe import PCSerial
        PCSerial._ENABLE_DEBUG = True
        attenobj = Primecamfe("/dev/ttyACM0")
        attenobj.set_atten(0, 2.3)
        self.assertEqual(attenobj.get_atten(0), 2.25)
        attenobj.set_atten(0, 2.49)
        self.assertEqual(attenobj.get_atten(0), 2.5)
        attenobj.set_atten(0, 2.1)
        self.assertEqual(attenobj.get_atten(0), 2.0)
        PCSerial._ENABLE_DEBUG = False




class InvalidInputTestWithAssertions(unittest.TestCase):
    def setUp(self):
        import src.primecamfe.PCSerial as lib
        lib._ASSERTIONS = True
        self.attenobj = Primecamfe("/dev/ttyACM0")

    def test_port_not_found(self):
        with self.assertRaises(ConnectionError):
            pcobj = Primecamfe("PORTYPORTTHATISNTREAL")

    def test_bad_atten(self):
        with self.assertRaises(AssertionError):
            a, b = self.attenobj.set_atten(0, 50)
            self.assertFalse(a)
            print(b)

    def test_bad_addr(self):
        with self.assertRaises(AssertionError):
            a, b =  self.attenobj.set_atten(9, 0)

        with self.assertRaises(AssertionError):
            a, b =  self.attenobj.set_atten(-1, 0)


class InvalidInputTestNoAssertions(unittest.TestCase):
    def setUp(self):
        import src.primecamfe.PCSerial as lib
        lib._ASSERTIONS = False
        lib._ENABLE_DEBUG = True
        self.attenobj = Primecamfe("/dev/ttyACM0")

    def test_addr_greater_than_7(self):
        a, b = self.attenobj.set_atten(8, 0)
        self.assertFalse(a)

    def test_addr_less_than_0(self):
        a, b = self.attenobj.set_atten(-1, 0)
        self.assertFalse(a)

    def test_errormsg_greater_than_7(self):
        a, b = self.attenobj.set_atten(8, 0)
        self.assertFalse(a)
        self.assertEqual(b, "FAIL, BAD ADDRESS NOT BETWEEN 0 THROUGH 7")

    def test_errormsg_less_than_0(self):
        a, b = self.attenobj.set_atten(-1, 0)
        self.assertFalse(a)
        self.assertEqual(b, "FAIL, BAD ADDRESS NOT BETWEEN 0 THROUGH 7")

    def test_atten_less_than_0(self):
        a, b = self.attenobj.set_atten(0, -5)
        self.assertFalse(a)
        self.assertEqual(b, "FAIL, ATTENUATION VALUE MUST BE BETWEEN 0 AND 31.75")

    def test_atten_greater_than_31p75(self):
        a, b = self.attenobj.set_atten(0, 100.2)
        self.assertFalse(a)
        self.assertEqual(b, "FAIL, ATTENUATION VALUE MUST BE BETWEEN 0 AND 31.75")

    @unittest.expectedFailure
    def test_atten_extreme_value(self):
        import src.primecamfe.PCSerial as lib
        lib._ASSERTIONS = False
        lib._ENABLE_DEBUG = True
        a, b, c = self.attenobj.set_atten(0, 10000.2)
        print(a,b,c)
        self.assertFalse(a)
        self.assertEqual(b, "FAIL, ATTENUATION VALUE MUST BE BETWEEN 0 AND 31.75")



if __name__ == '__main__':
    unittest.main()