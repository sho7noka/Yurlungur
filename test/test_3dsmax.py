# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Max
from yurlungur.tool import standalone


@unittest.skipUnless(_Max(), "Max is not found")
class TestMax(unittest.TestCase):
    def test_env(self):
        assert _Max()

    @unittest.skip("only runtime")
    def test_Max(self):
        standalone.maxpy("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        box = yr.YNode().create('box')
        print (box.name, box.id, box.attr('Width'), box.attrs)

        print (box.create('Mirror', offset=0.1))
        box.width.set(10)
        box.pos.set(yr.YVector(1, 100, 1))
        box.select()
        box('aaa')
        box = yr.YNode('aaa')
        print (box.geom())
        box2 = box.instance()
        print (box2.geom())

        yr.meta.eval('$%s.width = 20' % box.name)


if __name__ == '__main__':
    unittest.main()
