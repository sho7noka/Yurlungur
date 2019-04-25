# coding: utf-8
import platform, ctypes, os, sys

if platform.system() == "Windows":
    from comtypes.client import CreateObject, GetActiveObject

    try:
        app = GetActiveObject('Photoshop.Application')
    except WindowsError:
        app = CreateObject("Photoshop.Application")

# print app.Preferences.rulerUnits

# ドキュメント
try:
    print app.documents[0]
except IndexError:
    print app.documents.add(name)
except ctypes.ArgumentError:
    print app.activeDocument

# jpgFile = new File( "/Temp001.jpeg" )
jpgSaveOptions = app.JPEGSaveOptions()
jpgSaveOptions.embedColorProfile = True
# jpgSaveOptions.formatOptions = app.FormatOptions.STANDARDBASELINE
# jpgSaveOptions.matte = MatteType.NONE
jpgSaveOptions.quality = 1
app.activeDocument.saveAs("", jpgSaveOptions, True)


class Document(object):
    pass


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
