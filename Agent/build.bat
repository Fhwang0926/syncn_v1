::@echo off

::rmdir dist /s /q
::rmdir build /s /q
::del *.spec

pyinstaller --windowed --icon=C:\Remote_Project\syncn_v1\Agent\images\sync.ico --clean C:\Remote_Project\syncn_v1\Agent\SyncN.py

xcopy C:\Remote_Project\syncn_v1\Agent\images dist\SyncN
cd dist\SyncN
mkdir images
move sync.ico images
move sync.png images
cd.. 
copy %~dp0%RegStartProgram.bat SyncN /Y


SyncN.exe
