import time, os, threading, pdb
from PyQt5.QtCore import QThread, pyqtSignal

class Observer(QThread):
    # sendSignal = pyqtSignal()

    def __init__(self, path='', debug=False):
        super().__init__()
        self.is_run = False
        self.reset = False
        self.thread_run = False
        self.send_signal = False
        self.debug = debug
        # self.path = path
        self.path = path.dirSearch(dir="xpad", detailPath=os.environ['HOME'])[0]
        self.cnt = 0
        self.timestamp = os.path.getmtime(self.path)

    def stop(self):
        self.is_run = False

    def run(self):
        tmp = 0
        try:
            self.is_run = True
            while self.is_run:
                # file changing check
                if self.timestamp != os.path.getmtime(self.path):
                    # self.cnt = 0
                    self.reset = True
                    self.timestamp = os.path.getmtime(self.path)
                    # counter start
                    if self.thread_run == False:
                        counter = threading.Thread(target=self.counter)
                        counter.start()
        except Exception as e:
            print("Oberver run() method error, message: {0}\n".format(e))

    def counter(self, reset=False):
        try:
            self.thread_run = True
            while self.thread_run:
                if self.reset == True:
                    self.cnt = 0
                    self.reset = False
                if self.debug: print("After {0} second, start to sync ".format(5 - self.cnt))
                time.sleep(1)
                self.cnt += 1
                if self.cnt == 5:
                    self.send_signal = True
                    self.thread_run = False
                    if self.debug: print("Send signal emited\n")
                    return
        except Exception as e:
            print("Observer.py counter() method error, message: {0}\n".format(e))

if __name__ == '__main__':
    test = Observer(path="/Users/jeoninsuck/test.rtf", debug=True)
    test.run()
