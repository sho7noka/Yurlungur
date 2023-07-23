# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Toolbag


@unittest.skipUnless(_Toolbag(), "Marmoset is not found")
class TestMarmoset(unittest.TestCase):
    def test_env(self):
        assert _Toolbag()

    @unittest.skip("only runtime")
    def test_marmoset(self):
        yr.toolbag.run("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        yr.meta.file(new=1, f=1)


if __name__ == '__main__':
    unittest.main()
