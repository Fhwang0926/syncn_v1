#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com

import time, os, datetime
from PyQt5.QtCore import *
try:
    from Lib import Search
except ImportError:
    import Search

class signalThread(QThread):
    sync = pyqtSignal(bool)

    def __init__(self, sec=0, parent=None, debug=False):
        QThread.__init__(self)
        self.isRun = False
        self.debug = debug
        self.timestamp = 0;
        self.cnt = 0
        self.target = Search.PathSearcher().run()

    def __del__(self):
        if self.debug: print(".... end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False
        self.cnt = 0

    def run(self):
        try:
            self.cnt = 0
            self.isRun = True
            while self.isRun:
                if self.timestamp != os.path.getmtime(self.target): # change detected
                    self.cnt = 0;
                    self.timestamp = os.path.getmtime(self.target)
                    if self.debug: print("user writting")
                else:
                    if self.cnt > 10: 
                        if self.debug: print("sync emit")
                        self.sync.emit(True)
                        self.cnt = 0;
                    else:
                        if self.debug: print("Wait for Sync : ", 10 - self.cnt, " sec")
                        self.cnt +=1
                time.sleep(1)
        except Exception as e:
            self.stop()
            self.join()
            print("Error, check this {0}".format(e))

if __name__ == "__main__":
    th_signal = signalThread(debug=True)
    th_signal.start()
    while True:
        time.sleep(1)
        print("non blocking")
    

        