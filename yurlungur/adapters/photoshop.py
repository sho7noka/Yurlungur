# coding: utf-8
import platform, ctypes

if platform.system() == "Windows":
    if not __import__("comtypes"):
        import pip

        if getattr(pip, "main", False):
            pip.main(["install", "comtypes"])
        else:
            from pip import _internal

            _internal.main(["install", "comtypes"])

    from comtypes.client import GetActiveObject

    app = GetActiveObject("Photoshop.Application")


elif platform.system() == "Darwin":
    if not __import__("ScriptingBridge"):
        import pip

        if getattr(pip, "main", False):
            pip.main(["install", "pyobjc-framework-ScriptingBridge"])
        else:
            from pip import _internal

            _internal.main(["install", "pyobjc-framework-ScriptingBridge"])

    from ScriptingBridge import SBApplication

    app = SBApplication.applicationWithBundleIdentifier_("com.adobe.photoshop")


class Document(object):
    # ドキュメント
    try:
        print app.documents[0]
    except IndexError:
        print app.documents.add(name)
    except ctypes.ArgumentError:
        print app.activeDocument

    def layer(self):
        Layer


class Layer(object):
    # レイヤー
    app.activeDocument.activeLayer.name = "aaa"
    try:
        print app.activeDocument.artLayers["aaa"].kind
        layer = app.activeDocument.artLayers["aaa"]
        layer = app.activeDocument.artLayers[1]
        # app.activeDocument.artLayers["aaa"].delete()
    except ctypes.ArgumentError:
        layer = app.activeDocument.artLayers.Add()
        layer.name = "aaa"
        appSmartObjectLayer = 2  # from enum PsLayerKind
        # layer.Kind = appSmartObjectLayer


class Property(object):
    def add(self, name, *args):
        getattr(app.activeDocument.activeLayer, "apply%s" % name)(*args)

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
