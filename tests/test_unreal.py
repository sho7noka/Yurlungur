import doctest
import unittest

from yurlungur.core import standalone
from yurlungur.core.env import installed, Unreal

@unittest.skipUnless(installed("unreal"), "Unreal is not found")
class TestApp(unittest.TestCase):
    def test_app(self):
        pass
        # self.assertFalse(standalone.uepython("import sys; print sys.path"))

if __name__ == '__main__':
    unittest.main()