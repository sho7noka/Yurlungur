# -*- coding: utf-8 -*-

import doctest
import unittest
from yurlungur.core import app


class TestCore(unittest.TestSuite):
    def test_app(self):
        self.assertTrue(app.application == "standalone")


if __name__ == '__main__':
    unittest.main()
