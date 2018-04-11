import doctest
import unittest
import yurlungur as yr

class TestApp(unittest.TestCase):
    def test_maya(self):
        yr.application.mayapy("import sys; print sys.path")

    def test_max(self):
        yr.application.maxpy("import sys; print sys.path")

    def test_hou(self):
        yr.application.hython("import sys; print sys.path")

    def test_blender(self):
        yr.application.bpython("import bpy")


if __name__ == '__main__':
    unittest.main()
