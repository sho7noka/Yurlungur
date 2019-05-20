import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import installed, Houdini

@unittest.skipUnless(installed("houdini"), "Houdini is not found")
class TestHoudini(unittest.TestCase):
    def test_env(self):
        self.assertTrue(Houdini())

    def test_hou(self):
        yr.standalone.hython("import yurlungur as yr; print yr.name, yr.version")

    def test_node(self):
        yr.standalone.hython("import yurlungur as yr; print yr.YNode('obj')")

    def test_attr(self):
        yr.standalone.hython("import yurlungur as yr; yr.YNode('obj').create('geo').tx.set(5)")

    def test_file(self):
        yr.standalone.hython("import yurlungur as yr; yr.YFile.save('temp.hip')")

    def test_pdg(self):
        """PDG, Qt, yurlungur"""
        pass


if __name__ == '__main__':
    unittest.main()
