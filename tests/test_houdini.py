import doctest
import unittest
import yurlungur as yr
from yurlungur.core import enviroment
from yurlungur.core import standalone

@unittest.skipUnless(yr.installed("houdini"), "Houdini is not found")
class TestApp(unittest.TestCase):
    def test_env(self):
        self.assertTrue(enviroment.installed("houdini"))

    def test_hou(self):
        self.assertTrue(
            standalone.hython("import yurlungur as yr; print yr.name, yr.version")
        )

    def test_node(self):
        standalone.hython("import yurlungur as yr; print yr.YNode('obj')")

    def test_attr(self):
        standalone.hython("import yurlungur as yr; yr.YNode('obj').create('geo').tx.set(5)")

    def test_file(self):
        standalone.hython("import yurlungur as yr; yr.YFile.save('temp.hip')")


if __name__ == '__main__':
    unittest.main()
