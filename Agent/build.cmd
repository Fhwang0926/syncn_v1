echo off
cls
rmdir /s /q dist
rmdir /s /q build
del *.spec
xcopy Lib C:\Users\hdh09\AppData\Local\Programs\Python\Python36\Lib\Lib /E /Y
pyinstaller --onefile --nowindowed --hidden-import="C:\Users\hdh09\AppData\Local\Programs\Python\Python36\Lib\site-packages\PyQt5\sip.pyd" --icon="E:\Project\Agent\images\sync.ico" --clean -p ./build_windows SyncN.py
copy init.syncn dist\setting.syncn
xcopy images dist\images  /E /Y
echo on
cls
echo "Good, run"
cd dist
SyncN.exe
cd ..

