# coding: utf-8
import platform, ctypes

if platform.system() == "Windows":
    from comtypes.client import CreateObject, GetActiveObject

    try:
        app = GetActiveObject('Photoshop.Application')
    except WindowsError:
        app = CreateObject("Photoshop.Application")

elif platform.system() == "Darwin":
    from appscript import *

    papp = app("/Applications/Adobe Photoshop CC 2019/Adobe Photoshop CC 2019.app")
    print papp.print_, papp.open, papp.quit, papp.save


class Document(object):
    # ドキュメント
    try:
        print app.documents[0]
    except IndexError:
        print app.documents.add(name)
    except ctypes.ArgumentError:
        print app.activeDocument


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
