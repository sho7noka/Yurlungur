import doctest
import unittest
import yurlungur as yr

@unittest.skipIf(yr.installed("unreal"), "Unreal is not found")
class TestApp(unittest.TestCase):
    def test_app(self):
        self.assertFalse(yr.application.uepython("import sys; print sys.path"))

if __name__ == '__main__':
    unittest.main()