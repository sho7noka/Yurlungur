# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

from yurlungur.core import app


class TestCore(unittest.TestSuite):

    def test_app(self):
        self.assertTrue(app.application == "standalone")

    def test_vector(self):
        self.assertTrue(yr.YVector() == yr.YVector())


if __name__ == '__main__':
    unittest.main()
