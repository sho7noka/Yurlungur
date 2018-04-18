# -*- coding: utf-8 -*-
import unittest
import doctest
import yurlungur as yr


class TestCore(unittest.TestSuite):
    def test_vector(self):
        assert (yr.YVector() == yr.YVector())


class TestPerformance(unittest.TestSuite):
    def test_coverage(self):
        pass


if __name__ == '__main__':
    unittest.main()
