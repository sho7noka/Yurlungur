# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')

import yurlungur as yr
from yurlungur.core.env import _Unreal


@unittest.skipUnless(_Unreal(), "Unreal is not found")
class TestUnreal(unittest.TestCase):
    def test_app(self):
        assert _Unreal()

    @unittest.skip("only runtime")
    def test_read(self):
        with yr.UndoGroup("undo"):
            node = yr.YNode("Wall2")
            print (node.name)
            print (node.id)
            print (node.hidden)
            print (node.attr("hidden"))
            print (node.geom())

    @unittest.skip("only runtime")
    def test_write(self):
        with yr.UndoGroup("undo"):
            yr.YNode("").create()
            yr.YNode("Wall1").select()
            yr.YNode("Wall1").instance()
            # node.delete()

    @unittest.skip("only runtime")
    def test_file(self):
        print (yr.YFile().current)
        yr.YFile().save()
        yr.YFile().open()

    @unittest.skip("only runtime")
    def test_bridge(self):
        import yurlungur as yr

        yr.use("unity")

        # application = unity
        yr.unity.run()
        gobj = yr.Yobject("obj").create()
        gobj.order = 1
        f = yr.YFile().export()
        yr.unity.end()

        # yr.YFile.
        # import
        # (f)
        gobj.name = "aaa"
        yr.maya.shell("ls")


if __name__ == '__main__':
    unittest.main()
