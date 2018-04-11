cd 
wget "https://www.python.org/ftp/python/3.6.4/python-3.6.4-embed-amd64.zip" -O "epython_zip.zip"
Expand-Archive -Path epython_zip.zip -DestinationPath epython
python -m pip install pyside