import sys

sys.path.append('../yurlungur')
import yurlungur as yr

reload(yr)

yr.YNode("").create("TimeWarp")

if hasattr(meta, "knob"):
    b = nuke.toNode("aaa")
    k = nuke.Array_Knob("name", "label")
    b.addKnob(k)