import yurlungur as yr

__doc__ = """

https://docs.python.org/ja/2.7/reference/datamodel.html#customization
https://docs.python.jp/2.7/reference/datamodel.html#object.__new__

"""

import yurlungur as yr


if yr.Windows():
    print 1

if yr.Max:
    print 2

print yr.app.application

node = yr.YObject("pConeShape1")
node.attr("castsShadows").set(1)