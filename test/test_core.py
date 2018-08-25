# -*- coding: utf-8 -*-

import sys

sys.path.append('../yurlungur')

import doctest
import unittest
from yurlungur.core import app


class TestCore(unittest.TestSuite):

    def test_app(self):
        self.assertTrue(app.application == "standalone")

    def test_vector(self):
        self.assertTrue(yr.YVector() == yr.YVector())


if __name__ == '__main__':
    unittest.main()
