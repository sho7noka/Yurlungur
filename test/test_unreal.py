import doctest
import unittest

from yurlungur.core.env import installed, Unreal

@unittest.skipUnless(installed("unreal"), "Unreal is not found")
class TestUnreal(unittest.TestCase):
    def test_app(self):
        return True

if __name__ == '__main__':
    unittest.main()