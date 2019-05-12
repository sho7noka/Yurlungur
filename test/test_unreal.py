# coding: utf-8
import doctest
import unittest
import sys

sys.path.append('../yurlungur')


import sys; sys.path.append("C:/Users/sumioka-sho/Yurlungur"); import yurlungur as yr

from yurlungur.core.env import installed, Unreal


@unittest.skipUnless(installed("unreal"), "Unreal is not found")
class TestUnreal(unittest.TestCase):
    def test_app(self):
        raise Unreal()

    def test_read(self):
        with yr.UndoGroup("undo"):
            node = yr.YNode("Wall2")
            print node.name
            print node.id
            print node.hidden
            print node.attr("hidden")
            print node.geometry()

    def test_write(self):
        with yr.UndoGroup("undo"):
            yr.YNode("").create()
            yr.YNode("Wall1").select()
            yr.YNode("Wall1").instance()
            node.delete()

    def test_file(self):
        print yr.YFile().current
        yr.YFile().save()
        yr.YFile().open()


if __name__ == '__main__':
    unittest.main()
