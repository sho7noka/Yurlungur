import doctest
import unittest

import sys

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import installed, Substance


@unittest.skipUnless(installed("substance"), "Substance is not found")
class TestMaya(unittest.TestCase):
    def test_env(self):
        assert Substance()

    def test_maya(self):
        standalone.mayapy("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        uniform = yr.YNode().create("uniform")

        node = yr.YNode("Directional Warp")
        print(node, node.attr("$pixelsize"), node.attrs)
        normal = yr.YNode("Normal")
        print(normal)

        node.connect("unique_filter_output", normal, "inputNodeOutput.connector")
        print(node.parent())
        node.disconnect("unique_filter_output")
        print(node.parent())


if __name__ == '__main__':
    unittest.main()
