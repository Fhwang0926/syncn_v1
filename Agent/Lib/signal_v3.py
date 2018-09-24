#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com

import time, os,datetime
try:
    from Lib import Search
except ImportError:
    import Search
    pass

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt5.QtCore import *

# Event Hander Class 
class MyHandler(FileSystemEventHandler):
    def __init__(self, path, ext):
        
        self.monPath = path 
        self.monExt = ext
        print("-------Event Handler Start!!----------", self.getNow())
                
    def on_modified(self, event):
        print("[+] Files are Modified in the Target Folder !!!", self.getNow())
        print("  L___", event.event_type, event.src_path)
        # self.do_action(event)
            
    def on_created(self, event):
        print("[+] Files are Created in the Target Folder !!!", self.getNow())
        print("  L___", event.event_type, event.src_path)
        self.do_action(event)

    def getNow(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H-%M-%S")
    
    def get_fileinfo_from_fullpath(self,full_path):
        path, ext = os.path.splitext(full_path)
        name = os.path.basename(full_path)
        return path, name, ext
            
    def do_action(self,event):
        filePath, fileName, fileExt = self.get_fileinfo_from_fullpath(event.src_path)
        print("  L___path:%s, name:%s, ext:%s\n" % (filePath, fileName, fileExt))
        if self.monExt==fileExt: print("[+] type:{0}, Infected !! {1}".format(self.monExt, self.getNow()))
            

class signalThread(QThread):
    sync = pyqtSignal(bool)
    coroutine = pyqtSignal(bool)

    def __init__(self, sec=0, parent=None, debug=False):
        QThread.__init__(self)
        self.isRun = False
        self.debug = debug
        self.cnt = 0;
        self.setDir = Search.PathSearcher().getFindDir()

    def __del__(self):
        print(".... end thread.....")
        # self.wait()
    
    def stop(self):
        if not self.isRun:
            print("already stop")
            self.cnt = 0
            return
        else:
            print("real stop")
            self.isRun = False
            self.cnt = 0

    def start(self):
        if self.isRun:
            print("already thread")
            self.cnt = 0
            return
        else:
            print("real start")
            self.cnt = 0
            self.isRun = True
            self.run()

    def run(self):
        try:
            fileType = "sqlite"
            eventHandler = MyHandler(self.setDir, fileType)
           
            Core = Observer()
            Core.schedule(eventHandler, path=self.setDir, recursive=False)
            Core.start()

            # try:
                # while self.isRun:
                #     time.sleep(1)
                #     if self.debug: print("waitForUserAction")
            # except KeyboardInterrupt:
            #     Core.stop()
            # Core.join()
            print("non blocking")
        except Exception as e:
            print(e)
            pass

if __name__ == "__main__":
    
    th_signal = signalThread(debug=True)
    th_signal.start()
    print("run thread!!!")

        