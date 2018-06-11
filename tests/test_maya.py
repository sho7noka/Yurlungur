import doctest
import unittest
import yurlungur as yr
from yurlungur.core.env import installed, Maya
from yurlungur.core import standalone

@unittest.skipUnless(installed("maya"), "Maya is not found")
class TestApp(unittest.TestCase):
    def test_env(self):
        assert Maya()

    def test_maya(self):
        standalone.mayapy("import yurlungur as yr; print yr.name")

    @unittest.skip("only runtime")
    def test_cmds(self):
        yr.meta.file(new=1, f=1)
        cone, shape = yr.meta.polyCone()
        node = yr.YObject(shape)
        node.attr("castsShadows").set(1)


if __name__ == '__main__':
    unittest.main()
