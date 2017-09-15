import os
import subprocess

app_name = QCoreApplication.applicationName()
if app_name.startswith("Maya"): # Maya-2017
    app = "Maya"
elif app_name.startswith("houdinifx"): # houdinifx
    app = "Houdini"