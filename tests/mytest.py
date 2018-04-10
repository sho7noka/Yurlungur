import yurlungur as yr
import sys

__doc__ = """

https://docs.python.org/ja/2.7/reference/datamodel.html#customization
https://docs.python.jp/2.7/reference/datamodel.html#object.__new__

"""

# print yr.app.application
# node = yr.YObject("pConeShape1")
# node.attr("castsShadows").set(1)


print yr.Houdini()
print sys.executable

@yr.Maya
def aaa():
    return 2


print aaa()

# yr.application.mayapy("print 111")
yr.application.cli("--dlg")
