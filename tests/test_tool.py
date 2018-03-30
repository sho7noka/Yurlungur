import unittest
import doctest
import yurlungur as yr



class TestApp(unittest.TestCase):
    def test_env(self):
        print env.Max

    def test_maya(self):
        yr.application.mayapy("import sys; print sys.path")
#
#
# yr.application.maxpy("print 1")

if __name__ == '__main__':
    unittest.main()