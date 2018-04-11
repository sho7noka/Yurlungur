import doctest
import unittest
import yurlungur as yr
from yurlungur.core import enviroment
from yurlungur.core import standalone


class TestApp(unittest.TestCase):
    def test_env(self):
        self.assertTrue(enviroment.Maya())

    def test_maya(self):
        standalone.mayapy("import yurlungur as yr; print yr.name")

    def test_bin(self):
        self.assertTrue()

if __name__ == '__main__':
    unittest.main()