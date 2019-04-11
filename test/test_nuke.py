# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')
import yurlungur as yr


class TestResolve(unittest.TestSuite):

    def test_node(self):
        yr.YNode("").create("TimeWarp")

        if hasattr(yr.meta, "knob"):
            import nuke
            b = nuke.toNode("aaa")
            k = nuke.Array_Knob("name", "label")
            b.addKnob(k)
