# -*- coding: utf-8 -*-
import unittest
import doctest
import yurlungur as yr

class TestCore(unittest.TestSuite):
    def test_vector(self):
        assert (yr.YVector() == yr.YVector())

    def test_app(self):
        color = yr.YColor()
        matrix = yr.YMatrix()
        vec = yr.YVector()

if __name__ == '__main__':
    unittest.main()
