# coding: utf-8
import sys
import unittest

sys.path.append('../yurlungur')
import yurlungur as yr
from yurlungur.adapters import resolve


class TestResolve(unittest.TestSuite):

    def test_aaa(self):
        projects = resolve.Projects()
        print projects.timelines.tracks.comps
        print projects["Hellow"].timelines["g"].tracks

    def test_fscript(self):
        # comp起点とfusion起点の２つ
        # https://www.steakunderwater.com/VFXPedia/96.0.243.189/index1bea.html?title=Eyeon:Script/Reference/Applications/Fusion/Classes/Composition
        # print comp.GetToolList().values()[0].GetAttrs()
        # fpath = fusion.MapPath("/Users/shosumioka/Documents/DaVinci Resolve/aaa.comp")
        # mcomp = fusion.LoadComp(fpath)
        # pprint.pprint(mcomp.GetAttrs()['COMPS_FileName'])
        # mcomp.Save(), mcomp.Print(), mcomp.Close(), mcomp.Lock(), mcomp.Unlock(), mcomp.Paste()
        comp = resolve.Fusion().GetCurrentComp()
        bg1 = comp.Background()
        pl1 = comp.Plasma()
        mg1 = comp.Merge({"Background": bg1, "Foreground": pl1})
        comp.FindTool("MediaOut1").Input.ConnectTo(mg1.Output)
        for n in comp.ActiveTool.GetChildrenList().values():
            print n.Name
        # print comp.FindTool("MediaOut1").GetInputList()
        # comp.FindTool("MediaOut1").Input.ConnectTo()
        # print yr.YNode(mg1.Name).parent(), yr.YNode(mg1.Name).children()
        # yr.YNode("Loader1").connect()

    def test_fusion(self):
        mg1 = yr.YNode().create("Merge")
        print yr.YNode(mg1).children()
        paint = yr.YNode().create("Paint", 2, 1)
        print paint.id, paint.name, paint.attrs
        paint.hide()
        paint.instance()
        paint.select()
        paint.connect(yr.YNode("MediaOut1"))
        yr.YNode().create("Grain").delete()
        myblur = yr.YNode().create("Blur")
        mybg = yr.YNode().create("Background")
        mybg.connect(yr.YNode(myblur.name))
        mybg.Type.set("Vertical")
        myblur.XBlurSize.set(5.0)


if __name__ == "__main__":
    unittest.main()
