import sys
import unittest

sys.path.append("../yurlungur")

import yurlungur as yr
from yurlungur.core.env import _Photoshop


@unittest.skipUnless(_Photoshop(), "Photoshop is not found")
class TestPhotoshop(unittest.TestCase):

    def test_cmds(self):
        with yr.UndoGroup("undo"):
            yr.application.activate()
            node = yr.YObject("nnn")
            print node.opacity
            print node.name
            node.hide()
            node.select("aaa")
            print yr.YFile().current
            # node("nnn")

        yr.YObject("test").create("Normal")
        yr.YObject("test").AutoContrast()
        print(yr.YObject("test").parent())
        print(yr.YObject("test").blendMode)
        print(yr.YObject("test").attr("blendMode"))
        yr.YObject("test").opacity.set(3)
        yr.YObject("test")("test1")
        yr.YObject("test1").hide(False)
        print(yr.YObject("test1").instance())
        yr.YObject("test1").delete()
        print(yr.YObject("BBB").children())

    def test_file(self):
        yr.YFile().save("%USER%\\Documents\\Adobe\\ccd.psd")
        yr.YFile().open("%USER%\\Documents\\Adobe\\ccc.psd")
        print(yr.YFile().current)


if __name__ == "__main__":
    unittest.main()

# from ScriptingBridge import SBApplication
# app = SBApplication.applicationWithBundleIdentifier_("com.apple.itunes")
# p = {'name': 'Testing'}
# playlist = app.classForScriptingClass_("playlist").alloc().initWithProperties_(p)
# app.sources()[0].playlists().insertObject_atIndex_(playlist, 0)
