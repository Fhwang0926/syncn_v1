from Lib import Setting, MQ, NoteSql, Search
# from PyQt5.QtCore import QThread
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import win32file
import win32event
import win32con
import json

class signalThread(QThread):
    sync = pyqtSignal(bool)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.isRun = False
        self.cnt = 0;
        svc = Search.PathSearcher()
        self.path = svc.run()
        self.setDir = svc.getFindDir()
        self.handler = win32file.FindFirstChangeNotification(self.setDir, 0, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)

    def __del__(self):
        print(".... end thread.....")
        self.wait()
    
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
            while self.isRun:
                getSignal = win32event.WaitForSingleObject(self.handler, 1200)
                print(getSignal, self.cnt)
                if getSignal == win32con.WAIT_OBJECT_0:
                    # change detected
                    self.cnt = 0;
                    win32file.FindNextChangeNotification(self.handler)
                elif getSignal == win32con.WAIT_FAILED:
                    # self.th.stop()
                    print("Occured the Error")
                else:
                    print("WTF")
                    if self.cnt > 10:
                        self.sync.emit(True)
                        self.cnt = 0;
                    else:
                        self.cnt +=1
        except Exception as e:
            print(e)
            pass
        
class mqSendThread(QThread):

    def __init__(self, sec=0, parent=None):
        super().__init__()
        try:
            self.config = Setting.syncn("setting.syncn")
            self.ch = MQ.MQ()
            self.DAO = NoteSql.DAO()
        except Exception as e:
            print(e)
            pass
        
    def run(self):
        # self.sec_changed.emit('time (secs)：{}'.format(self.sec))
        print("send?", type(json.dumps(self.DAO.read())))
        self.ch.publishExchange("msg", self.ch.queue, json.dumps(self.DAO.read()))
        self.wait()

class mqreciveThread(QThread):
    
    def __init__(self, sec=0, parent=None):
        super().__init__()
        try:
            self.isRun = False
            self.sec = 0
            self.config = Setting.syncn("setting.syncn")
            self.ch = MQ.MQ()
        except Exception as e:
            print(e)
            pass
        
        # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

    def __del__(self):
        print(".... end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

    def start(self):
        self.isRun = True
        self.run()

    def run(self):
        while self.isRun:
            # self.sec_changed.emit('time (secs)：{}'.format(self.sec))
            print("hello")
            self.sleep(5)
            self.sec += 1

    # @pyqtSlot()
    # def add_sec(self):
    #     print("add_sec....")
    #     self.sec += 100

    # @pyqtSlot("PyQt_PyObject")    # @pyqtSlot(object) 도 가능..
    # def recive_instance_singal(self, inst):
        # print(inst.name)

class dataThread(QThread):
    
    def __init__(self, sec=0, parent=None):
        super().__init__()
        try:
            self.isRun = False
            self.config = Setting.syncn("setting.syncn")
            self.DAO = NoteSql.DAO()
        except Exception as e:
            print(e)
            pass
        
        # self.main.add_sec_signal.connect(self.add_sec)   # 이것도 작동함. # custom signal from main thread to worker thread

    def __del__(self):
        print(".... end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

    def start(self):
        self.isRun = True
        self.run()

    def run(self):
        while self.isRun:
            # self.sec_changed.emit('time (secs)：{}'.format(self.sec))
            print("hello")
            self.sleep(5)
            self.sec += 1

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = MyMain()
    app.exec_()