# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Modo


@unittest.skipUnless(_Modo(), "Modo is not found")
class TestModo(unittest.TestCase):
    def test_env(self):
        assert _Modo()

    def test_modo(self):
        yr.modo.shell("")


if __name__ == '__main__':
    unittest.main()
