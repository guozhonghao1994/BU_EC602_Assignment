"""
Example of using unittest to test a class. 
The class begin tested is Complex
"""
import unittest

from model_complex import Complex


class ComplexTestCase(unittest.TestCase):
    """unit testing for polynomials"""

    def setUp(self):
        pass

    def test_init(self):
        z = Complex()
        self.assertIsInstance(z, Complex)

    def test_eq(self):
        z = Complex(3, 5)
        w = 3 + 5j
        self.assertEqual(z, w)

    def tearDown(self):
        "tear down"


if __name__ == '__main__':
    unittest.main()
