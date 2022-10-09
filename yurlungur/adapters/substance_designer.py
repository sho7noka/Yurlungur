# coding: utf-8
import sys as __sys

try:
    import sd
    context = sd.getContext()
    app = context.getSDApplication()
    manager = app.getPackageMgr()

    if getattr(app, "getUIMgr", False):
        graph = app.getUIMgr().getCurrentGraph()
        UndoGroup = sd.api.SDHistoryUtils.UndoGroup
        qt = app.getQtForPythonUIMgr()
    else:
        graph = manager.getUserPackages()[0].getChildrenResources(True)[0]

    __sys.modules[__name__] = __sys.modules["sd.api"]

    import yurlungur
    for obj in [obj for obj in dir(yurlungur) if obj[0] != "_" and obj != "Qt"]:
        setattr(__sys.modules[__name__], obj, getattr(yurlungur, obj))


    def node_img(id, path):
        """accesser for QImage"""
        import sd.api
        node = graph.getNodeFromId(id)
        out = node.getProperties(sd.api.sdproperty.SDPropertyCategory.Output)[0]
        vtex = node.getPropertyValue(out)

        img = sd.api.qtforpythonuimgrwrapper.QtForPythonUIMgrWrapper(app.getUIMgr()).convertSDTextureToQImage(vtex.get())
        if path:
            img.save(path)
        return img


except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, quit, _ = __App("substance_designer")._actions

    __all__ = ["run", "quit"]
