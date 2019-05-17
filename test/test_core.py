# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core import application


class TestCore(unittest.TestSuite):

    def test_app(self):
        self.assertTrue(application == "standalone")

    def test_vector(self):
        self.assertTrue(yr.YVector() == yr.YVector())


if __name__ == '__main__':
    unittest.main()
