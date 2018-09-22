from PyQt5.QtCore import *
import Search
import win32file
import win32event
import win32con

class threadSignal(QThread):
    sync = pyqtSignal(bool)

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.isRun = False
        self.cnt = 0;
        svc = Search.PathSearcher()
        self.path = svc.run()
        self.setDir = svc.getFindDir()
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)
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
        
        while self.isRun:
            getSignal = win32event.WaitForSingleObject(self.handler, 1000)
            print(getSignal, self.cnt)
            if getSignal == win32con.WAIT_OBJECT_0:
                print("2", self.cnt)

                # change detected
                print("Changed File", "start")
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


if __name__ == '__main__':
    threadSignal().start()