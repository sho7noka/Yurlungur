# -*- coding: utf-8 -*-
import os
import platform

def Windows():
    return platform.system() == "Windows"
def Linux():
    return platform.system() == "Linux"
def MacOS():
    return platform.system() == "Darwin"


for root, folders, files in os.walk("C:\Program Files\Autodesk\Maya2017"):
    for file in files:
        if file.endswith(".exe"):
            print file

print os.environ.get("HIP")