# import argparse
import sys
import subprocess

class Initialize(object):

    def __init__(self, application):
        pass
    
    def call(self, ):
        subprocess.call(
            "C:\Program Files\Autodesk\Maya2017\bin\mayapy.exe -c \"{}\"".format(pystr)
        )

    def execfile(self, *args, **kwargs):
        pass

    def find_application(self):
        if sys.platform == 'linux':
            pass
        if sys.platform == 'win32':
            pass
        if sys.platform == 'cygwin':
            pass
        if sys.platform == 'darwin':
            pass

    def set_application(self, app_root):
        pass

    
    

def main():
    # argparse
    # subprocess.call("hython {}".format(""))


    import maya.standalone
    maya.standalone.initialize(name='python')


    maya.standalone.uninitialize()

    
if __name__ == '__main__':
    main()