import doctest
import unittest

import yurlungur

class TestApp(unittest.TestCase):
    def test_maya(self):
        yurlungur.application.mayapy("import sys; print sys.path")

    def test_max(self):
        yurlungur.application.maxpy("import sys; print sys.path")

    def test_hou(self):
        yurlungur.application.hython("import sys; print sys.path")

    def test_blender(self):
        yurlungur.application.bpython("import bpy")


if __name__ == '__main__':
    unittest.main()
