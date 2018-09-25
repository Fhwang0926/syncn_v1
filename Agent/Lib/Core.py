try:
    from Lib import Setting, MQ, NoteSql, Search, Signal
except ImportError:
    import Setting
    import MQ
    import NoteSql
    import Search
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import json
import time


class signalThread(QThread):
    sync = pyqtSignal(bool)
    
    def __init__(self, debug=False):
        super().__init__()
        
        self.isRun = False
        self.debug = debug
        self.timestamp = 0;
        self.cnt = 0
        self.target = Search.PathSearcher().run()
        self.signal = Signal.signal(debug=self.debug)
        self.signalRunner = self.signal.connect()

    def __del__(self):
        if self.debug: print(".... end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False
        self.cnt = 0

    def run(self):
        try:
            self.isRun = next(self.signalRunner)
            while self.isRun:
                print("isRun = True")
                self.sync.emit(True)
                self.signalRunner.send(0)
                
                time.sleep(1)
        except Exception as e:
            self.stop()
            self.join()
            print("Error, check this {0}".format(e))


class mqSendThread(QThread):

    def __init__(self, debug=False):
        QThread.__init__(self)
        try:
            self.debug = debug
            self.config = Setting.syncn("../setting.syncn")
            self.ch = MQ.MQ(debug=self.debug)
            self.DAO = NoteSql.DAO()
        except Exception as e:
            print(e)
            pass

    def __del__(self):
        if self.debug: print(".... end thread.....")
        self.wait()
        
    def run(self, msg=""):
        print("msg : ", (msg))
        if msg:
            print("WTF")
            pass
        else:
            if self.debug: print("send?", type(json.dumps(self.DAO.read())))
            self.ch.publishExchange("msg", self.ch.queue, json.dumps(self.DAO.read()))
            if self.debug: print("publishExchange", time.time())
            # self.ch.publishExchange("msg", self.ch.queue, json.dumps("test"))

class mqReciveThread(QThread):
    
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

    def run(self):
        self.isRun = True
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

    def run(self):
        self.isRun = True
        while self.isRun:
            # self.sec_changed.emit('time (secs)：{}'.format(self.sec))
            print("hello")
            self.sleep(5)
            self.sec += 1

if __name__ == "__main__":
    th_mq = mqSendThread()
    th_mq.start()
    while 1:
        time.sleep(1)