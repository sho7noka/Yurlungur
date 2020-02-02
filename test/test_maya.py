# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Maya


@unittest.skipUnless(_Maya(), "Maya is not found")
class TestMaya(unittest.TestCase):
    def test_env(self):
        assert _Maya()

    def test_maya(self):
        yr.standalone.mayapy("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        yr.meta.file(new=1, f=1)
        cone, shape = yr.meta.polyCone()
        node = yr.YObject(shape)
        node.attr("castsShadows").set(1)


if __name__ == '__main__':
    unittest.main()
