# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import installed, C4D


@unittest.skipUnless(installed("c4d"), "C4D is not found")
class TestC4D(unittest.TestCase):
    @unittest.skip("only runtime")
    def test_env(self):
        assert C4D()

    @unittest.skip("only runtime")
    def test_c4d(self):
        yr.standalone.c4dpy("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        yr.YObject("").create("Ocube")
        yr.YObject("立方体")("box")

        caps = yr.YObject("box")
        print(caps.attr("PRIM_CUBE_SEP").value)
        print(caps.PRIM_CUBE_SEP.value)
        caps.attr("PRIM_CUBE_SEP").set(True)
        caps.PRIM_CUBE_FRAD.set(4)

        with yr.UndoGroup("undo"):
            caps.delete()

    @unittest.skip("only runtime")
    def test_file(self):
        pass


def main():
    caps = yr.YObject("立方体")
    caps.instance()
    # print(caps.attrs)
    # caps.select()


if __name__ == '__main__':
    main()  # unittest.main()
