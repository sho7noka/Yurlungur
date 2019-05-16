import sys

sys.path.append("../yurlungur")

import doctest
import unittest

# import yurlungur as yr
# from yurlungur.core.env import installed, Photoshop


# @unittest.skipUnless(installed("photoshop"), "Photoshop is not found")
# class TestPhotoshop(unittest.TestCase):
#     def test_env(self):
#         assert Photoshop()
#
#     @unittest.skip("only runtime")
#     def test_cmds(self):
#         yr.YNode("test").create("Normal")
#         yr.YNode("test").AutoContrast()
#         print(yr.YNode("test").parent())
#         print(yr.YNode("test").blendMode)
#         print(yr.YNode("test").attr("blendMode"))
#         yr.YNode("test").opacity.set(3)
#         yr.YNode("test")("test1")
#         yr.YNode("test1").hide(False)
#         print(yr.YNode("test1").instance())
#         yr.YNode("test1").delete()
#         print(yr.YNode("BBB").children())
#
#     @unittest.skip("only runtime")
#     def test_file(self):
#         yr.YFile().save("%USER%\\Documents\\Adobe\\ccd.psd")
#         yr.YFile().open("%USER%\\Documents\\Adobe\\ccc.psd")
#         print(yr.YFile().current)
#
# if __name__ == "__main__":
# unittest.main()

from yurlungur.adapters import photoshop

app = photoshop.app
doc = photoshop.Document()
app.close(app)
print app.get(), app.currentDocument().currentLayer().name()

# state = doc.historyState().get()
# for layer in app.currentDocument().artLayers():
#     layer.setValue_forKey_("T", "name")
#     layer.setValue_forKey_(True, "visible")
#     layer.setValue_forKey_(30, "opacity")
#     # layer.setValue_forKey_(3, "blendMode")
# doc.historyState().setTo_(state)
