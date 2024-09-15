@echo off
@title Compiling desktop-groups...

rem Install dependencies
echo Installing dependencies...
@py -m pip install --upgrade pip
@py -m pip install --upgrade pyinstaller

rem Build and install Python package
echo Installing desktop-groups as python package...
@py -m pip install --upgrade .

rem Build desktop-groups executable
echo Building desktop_groups executable...
pyinstaller --noconfirm --log-level=WARN --onefile --windowed --name=desktop-groups --icon=src\desktop_groups\assets\img\desktopgroups256px.ico --collect-all=desktop_groups --hidden-import=customtkinter --hidden-import=pillow --hidden-import=jsonschema --hidden-import=argparse --hidden-import=icoextract src\run.py
echo Process finished. Press any key to continue...
pause