import doctest
import unittest
import yurlungur as yr
from yurlungur.core import enviroment
from yurlungur.core import standalone

@unittest.skipUnless(yr.installed("houdini"), "Houdini is not found")
class TestApp(unittest.TestCase):

    def test_hou(self):
        standalone.hython("import yurlungur as yr; print yr.name")


if __name__ == '__main__':
    unittest.main()
