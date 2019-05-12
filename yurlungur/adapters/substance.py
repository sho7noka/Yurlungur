# coding: utf-8
import sd
from sd.api.sdproperty import SDPropertyCategory

context = sd.getContext()
sd_app = context.getSDApplication()

manager = sd_app.getPackageMgr()
graph = sd_app.getUIMgr().getCurrentGraph()
if not graph:
    graph = manager.getUserPackages()[0].getChildrenResources(True)[0]

UndoGroup = sd.api.SDHistoryUtils.UndoGroup
