::@echo off

::rmdir dist /s /q
::rmdir build /s /q
::del *.spec

pyinstaller --icon=images\sync.ico --clean SyncN.py

xcopy images dist\SyncN
cd dist\SyncN
mkdir images
move sync.ico images
move sync.png images
cd.. 
copy %~dp0%RegStartProgram.bat SyncN /Y


SyncN.exe
