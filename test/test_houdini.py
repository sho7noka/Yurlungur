import doctest
import unittest

import sys

sys.path.append('../yurlungur')

from yurlungur.core.env import installed, Houdini

@unittest.skipUnless(installed("houdini"), "Houdini is not found")
class TestHoudini(unittest.TestCase):
    def test_env(self):
        self.assertTrue(installed("houdini"))

    def test_hou(self):
        standalone.hython("import yurlungur as yr; print yr.name, yr.version")

    def test_node(self):
        standalone.hython("import yurlungur as yr; print yr.YNode('obj')")

    def test_attr(self):
        standalone.hython("import yurlungur as yr; yr.YNode('obj').create('geo').tx.set(5)")

    def test_file(self):
        standalone.hython("import yurlungur as yr; yr.YFile.save('temp.hip')")


if __name__ == '__main__':
    unittest.main()
