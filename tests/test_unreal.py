import doctest
import unittest
import yurlungur as yr
from yurlungur.core.env import installed, Unreal
from yurlungur.core import standalone

@unittest.skipUnless(installed("unreal"), "Unreal is not found")
class TestApp(unittest.TestCase):
    def test_app(self):
        pass
        # self.assertFalse(standalone.uepython("import sys; print sys.path"))

if __name__ == '__main__':
    unittest.main()