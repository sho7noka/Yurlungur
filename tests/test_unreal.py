import doctest
import unittest
import yurlungur as yr

@unittest.skipIf(yr.Unreal(), "Unreal is not found")
class TestApp(unittest.TestCase):
    def test_app(self):
        yr.application.uepython("import sys; print sys.path")

if __name__ == '__main__':
    unittest.main()