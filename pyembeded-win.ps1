Invoke-WebRequest "https://www.python.org/ftp/python/3.6.4/python-3.6.4-embed-amd64.zip" -O "epython_zip.zip"
Expand-Archive -Path epython_zip.zip -DestinationPath epython
cd epython
Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
python get-pip.py
python -m pip install pyside2