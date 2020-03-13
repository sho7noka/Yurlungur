# embeded python
Invoke-WebRequest "https://www.python.org/ftp/python/3.6.4/python-3.6.4-embed-amd64.zip" -O "Python.zip"
Expand-Archive -Path Python.zip -DestinationPath Python
Remove-Item Python.zip

# get pip
Set-Location Python
Invoke-WebRequest "https://bootstrap.pypa.io/get-pip.py" -OutFile "get-pip.py"
./python.exe get-pip.py
Remove-Item get-pip.py

# set path
$pth = @"
python36.zip
.
Lib/site-packages
Scripts

# Uncomment to run site.main() automatically
#import site
"@
New-Item python36._pth -itemType File -Force -Value $pth

#install module
./python.exe -m pip install yurlungur

