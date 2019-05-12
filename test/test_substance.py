# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')
import sys;

sys.path.append("/Users/shosumioka/Yurlungur");
import yurlungur as yr
from yurlungur.core.env import installed, Substance


@unittest.skipUnless(installed("substance"), "Substance is not found")
class TestSubstance(unittest.TestCase):
    def test_env(self):
        assert Substance()

    @unittest.skip("only runtime")
    def test_cmds(self):
        with yr.UndoGroup("undo"):
            node = yr.YNode().create("uniform")

            print(node, node.attr("$pixelsize"), node.attrs)
            normal = yr.YNode().create("normal")
            print(normal)

            node.connect("unique_filter_output", normal, "inputNodeOutput.connector")
            print(node.parent())
            node.disconnect("unique_filter_output")
            print(node.parent())

    def test_file(self):
        yr.YFile.open("")


if __name__ == '__main__':
    unittest.main()
