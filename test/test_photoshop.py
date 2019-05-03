import doctest
import unittest

import sys

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import installed, Photoshop


@unittest.skipUnless(installed("photoshop"), "Photoshop is not found")
class TestPhotoshop(unittest.TestCase):
    def test_env(self):
        assert Photoshop()

    @unittest.skip("only runtime")
    def test_cmds(self):
        yr.meta.file(new=1, f=1)
        cone, shape = yr.meta.polyCone()
        node = yr.YObject(shape)
        node.attr("castsShadows").set(1)


if __name__ == '__main__':
    unittest.main()
