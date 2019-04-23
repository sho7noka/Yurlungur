import platform, ctypes

if platform.system() == "Windows":
    from comtypes.client import CreateObject, GetActiveObject

    ps = GetActiveObject('Photoshop.Application')

elif platform.system() == "Darwin":
    from appscript import app

    ps = app('/Applications/Adobe Photoshop CC 2018/Adobe Photoshop CC 2018.app')

name = "aaa"
print "Photoshop" in ps.name

# getByName, typename 使えない
# /document/layer
print ps.Preferences.rulerUnits

# ドキュメント
try:
    print ps.documents[0]
except IndexError:
    print ps.documents.add(name)
except ctypes.ArgumentError:
    print ps.activeDocument

# レイヤー
ps.activeDocument.activeLayer.name = "aaa"
try:
    print ps.activeDocument.artLayers["aaa"].kind
    layer = ps.activeDocument.artLayers["aaa"]
    layer = ps.activeDocument.artLayers[1]
    # ps.activeDocument.artLayers["aaa"].delete()
except ctypes.ArgumentError:
    layer = ps.activeDocument.artLayers.Add()
    layer.name = "aaa"
    psSmartObjectLayer = 2  # from enum PsLayerKind
    # layer.Kind = psSmartObjectLayer

# フィルター/プロパティ
ps.activeDocument.activeLayer.blendMode
ps.activeDocument.activeLayer.opacity
ps.activeDocument.activeLayer.fillOpacity
ps.activeDocument.activeLayer.allLocked
ps.activeDocument.activeLayer.visible
ps.activeDocument.activeLayer.applyblur()
# ps.activeDocument.activeLayer.applyStyle("Embs")
return


class File(os.path):
    def getFiles(self):
        pass

    def fullName(self):
        pass

    def path(self):
        pass


# jpgFile = new File( "/Temp001.jpeg" )
jpgSaveOptions = ps.JPEGSaveOptions()
jpgSaveOptions.embedColorProfile = True
# jpgSaveOptions.formatOptions = ps.FormatOptions.STANDARDBASELINE
# jpgSaveOptions.matte = MatteType.NONE
jpgSaveOptions.quality = 1
ps.activeDocument.saveAs("", jpgSaveOptions, True)


def create(name):
    layer = ps.activeDocument.artLayers.Add()
    layer.name = "aaa"
    psSmartObjectLayer = 2  # from enum PsLayerKind
    layer.Kind = psSmartObjectLayer


def __getattr__(k):
    getattr(ps.activeDocument, k)


def attr(k):
    if hasattr(ps.activeDocument, k):
        print ps.activeDocument.width, hasattr(ps.activeDocument, k)
    if hasattr(ps.Preferences, k):
        print hasattr(ps.Preferences, k)


def rename(name):
    setattr(ps.activeDocument.activeLayer, "name", name)


def remove():
    ps.activeDocument.activeLayer.delete()


def duplicate():
    ps.activeDocument.activeLayer.duplicate()


def add(name, *args):
    getattr(ps.activeDocument.activeLayer, "apply%s" % name)(*args)


def select(name):
    print ps.activeDocument.selection.deselect()
    sel_area = ((50, 60), (150, 60), (150, 120), (50, 120))
    psReplaceSelection = 1  # from enum PsSelectionType
    ps.activeDocument.Selection.Select(sel_area, psReplaceSelection, 5.5, False)
