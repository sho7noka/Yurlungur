import doctest
import unittest
import yurlungur as yr
from yurlungur.core.env import installed, Blender
from yurlungur.core import standalone

@unittest.skipUnless(installed("Blender"), "Blender is not found")
class TestApp(unittest.TestCase):
    def test_env(self):
        self.assertTrue(installed("Blender"))

    def test_blender(self):
        standalone.bpython("import yurlungur as yr; print (yr.name)")

    @unittest.skip("only runtime")
    def test_cmds(self):
        self.assertTrue(yr.YObject("Cube"))


if __name__ == '__main__':
    unittest.main()
