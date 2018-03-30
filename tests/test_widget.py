import doctest
import unittest
import yurlungur as yr
import yurlungur.core.enviroment as env

class TestApp(unittest.TestCase):
    def test_env(self):
        env.Max

    def test_maya(self):
        yr.application.mayapy("import sys; print sys.path")

    def test_max(self):
        yr.application.maxpy("import sys; print sys.path")

    def test_hou(self):
        yr.application.hython("import sys; print sys.path")

    def test_atandalone(self):
        yr.YurPrompt()