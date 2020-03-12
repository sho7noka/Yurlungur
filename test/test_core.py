# -*- coding: utf-8 -*-
import sys
import unittest

sys.path.append('../yurlungur')

from yurlungur.core import application
from yurlungur.core.proxy import YVector


class TestCore(unittest.TestSuite):

    def test_app(self):
        self.assertTrue(application == "standalone")

    def test_cli(self):
        import yurlungur
        print(yurlungur.blender.shell("print(2)"))

    def test_vector(self):
        self.assertTrue(YVector() == YVector())


if __name__ == '__main__':
    unittest.main()
