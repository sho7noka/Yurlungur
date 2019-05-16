# coding: utf-8
import platform
from yurlungur.core import env

if platform.system() == "Windows":
    if not env.__import__("comtypes"):
        import pip

        if getattr(pip, "main", False):
            pip.main(["install", "comtypes"])
        else:
            from pip import _internal

            _internal.main(["install", "comtypes"])

    from comtypes.client import GetActiveObject

    app = GetActiveObject("Photoshop.Application")


elif platform.system() == "Darwin":
    if not env.__import__("ScriptingBridge"):
        import pip

        if getattr(pip, "main", False):
            pip.main(["install", "pyobjc-framework-ScriptingBridge"])
        else:
            from pip import _internal

            _internal.main(["install", "pyobjc-framework-ScriptingBridge"])

    from ScriptingBridge import SBApplication

    app = SBApplication.applicationWithBundleIdentifier_("com.adobe.photoshop")


class Document(object):
    """
    >>> app.Document[0].layer.add()
    """

    def __init__(self):
        self.document = (
            app.activeDocument if env.Windows() else app.currentDocument()
        )

    def __getitem__(self, val):
        self.document = app.documents[val]

    def set(self):
        pass

    def layer(self):
        return Layer(self.document)

    def historyState(self):
        return (
            self.document.activeHistoryState if env.Windows()
            else self.document.currentHistoryState()
        )


class Layer(object):

    def __init__(self, document):
        self.document = document
        self.layer = (
            self.document.activeLayer
            if env.Windows() else self.document.currentLayer()
        )

    def __getitem__(self, val):
        self.layer = (
            self.document.artLayers[val]
            if env.Windows() else self.document.artLayers()[val]
        )

    def add(self):
        pass

    def rm(self):
        pass

    def set(self):
        print app.activeDocument.artLayers["aaa"].kind
        layer = app.activeDocument.artLayers["aaa"]
        layer = app.activeDocument.artLayers[1]
        # app.activeDocument.artLayers["aaa"].delete()
        layer = app.activeDocument.artLayers.Add()
        layer.name = "aaa"
        appSmartObjectLayer = 2  # from enum PsLayerKind
        # layer.Kind = appSmartObjectLayer


class Property(object):
    def add(self, name, *args):
        getattr(app.activeDocument.activeLayer, "apply%s" % name)(*args)

    def set(self):
        # フィルター/プロパティ
        app.activeDocument.activeLayer.blendMode
        app.activeDocument.activeLayer.opacity
        app.activeDocument.activeLayer.fillOpacity
        app.activeDocument.activeLayer.allLocked
        app.activeDocument.activeLayer.visible
        app.activeDocument.activeLayer.applyblur()
        # app.activeDocument.activeLayer.applyStyle("Embs")


def do(cmd):
    """
    photoshop command runner
    """
    assert len(cmd) == 4 and ("'" not in cmd)
    app.DoJavaScript("""
        executeAction(charIDToTypeID("%s"), undefined, DialogModes.NO);
    """ % cmd)
