import doctest
import unittest
import yurlungur as yr

@unittest.skipIf(yr.Houdini(), "Houdini is not found")
class TestApp(unittest.TestCase):

    def test_hou(self):
        yr.application.hython("import sys; print sys.path")


if __name__ == '__main__':
    unittest.main()
