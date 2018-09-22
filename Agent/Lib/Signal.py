import os
import time
import threading
import Search

import win32file
import win32event
import win32con


class Signal():
    def __init__(self):
        self.setPath = Search.PathSearcher().run()
        self.setDir = Search.PathSearcher().getFindDir()
        # self.setDir = "C:\\test"
        self.path = self.setPath
        self.timer_is_runing = False
        self.roop_is_runing = False
        print("Watching %s at %s" % (self.path, time.asctime()))

    def run(self):
        self.roop_is_runing = True
        handler = self.lastWriteSignal()
        while self.roop_is_runing:
            self.sendSignal = win32event.WaitForSingleObject(handler, 500)
            print(self.sendSignal)
            if self.sendSignal == win32con.WAIT_OBJECT_0:
                print("Changed File")


                if self.timer_is_runing == False:
                    self.timerStart()
                # elif self.timer_is_runing == True:
                #     self.timerStop()


                win32file.FindNextChangeNotification(handler)
            elif self.sendSignal == win32con.WAIT_FAILED:
                print("Occured the Error")

    def timerStart(self):
        self.timer = threading.Timer(10, self.sendQueue)
        self.timer.start()
        self.timer_is_runing = True

    def timerStop(self):
        self.timer.cancel()
        self.timer_is_runing = False

    def sendQueue(self):
        pass

    def nameChangeSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir, 0, win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
        return self.handler

    def dirChangeSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_DIR_NAME)
        return self.handler

    def attrChangeSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES)
        return self.handler

    def sizeChangeSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_SIZE)
        return self.handler

    def lastWriteSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_LAST_WRITE)
        return self.handler

    def securityChangeSignal(self):
        self.handler = win32file.FindFirstChangeNotification(self.setDir,
                                                             0,
                                                             win32con.FILE_NOTIFY_CHANGE_SECURITY)
        return self.handler

    def deleteSignal(self):
        pass

    def quitSignal(self):
        pass

    def stopSync(self):
        self.roop_is_runing = False


if __name__ == '__main__':
    Signal().run()