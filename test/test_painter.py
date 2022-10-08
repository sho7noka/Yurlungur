# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _SubstancePainter


@unittest.skipUnless(_SubstancePainter(), "Substance Paiinter is not found")
class TestSubstance(unittest.TestCase):

    @unittest.skip("only runtime")
    def test_cmds(self):
        pass

    @unittest.skip("only runtime")
    def test_file(self):
        yr.File.open("")


if __name__ == '__main__':
    unittest.main()
