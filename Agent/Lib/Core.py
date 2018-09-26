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
import requests


class signalThread(QThread):
    syncSignal = pyqtSignal(bool)
    
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
                self.syncSignal.emit(True)
                self.signalRunner.send(0)
                time.sleep(1)
        except Exception as e:
            self.stop()
            self.join()
            print("signalThread, check this {0}".format(e))

class mqSendThread(QThread):
    msgRemoveSignal = pyqtSignal(bool)
    def __init__(self, debug=False):
        QThread.__init__(self)
        try:
            self.debug = debug
            self.msg = ''
            self.DAO = NoteSql.DAO()
        except Exception as e:
            print("mqSendThread, check this {0}".format(e))
            pass

    def __del__(self):
        if self.debug: print(".... mqSendThread end.....")
        self.wait()
        
    def run(self):
        try:
            ch = MQ.MQ()
            if self.debug: print("send?", type(json.dumps(self.DAO.read())))
            msg = self.msg if self.msg else json.dumps(self.DAO.read())
            opt = { "type" : "cmd" } if self.msg else { "type" : "msg" }
            headers = { "host" : ch.config["id"] } if self.msg else ''
            ch.publishExchange("msg", ch.queue, msg, opt=opt, head=headers)
            if self.debug:
                print("push : {0} {1} {2} bytes {3} {4}".format(time.time(), "msg", ch.queue, len(msg), opt, headers))
            self.msg = ''
            ch.worker(self.worker, ch.queue)
        except Exception as e:
            print("mqSendThread, check this {0}".format(e))
    
    def worker(self, ch, method, properties, msg):
        try:
            ch.basic_ack(delivery_tag = method.delivery_tag)
            ch.close()
        except Exception as e:
            print("worker, check this {0}".format(e))

class mqReciveThread(QThread):
    exitSignal = pyqtSignal(bool)
    syncSignal = pyqtSignal(bool)

    def __init__(self, debug=False):
        super().__init__()
        try:
            self.isRun = False
            self.debug = debug
            self.ch = MQ.MQ()
        except Exception as e:
            print("mqReciveThread, check this {0}".format(e))
            pass

    def __del__(self):
        print(".... mqReciveThread end.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

    def run(self):
        self.isRun = True
        try:
            queueInfo = requests.get(url="{0}/info/queue/{1}".format(self.ch.config["service"], self.ch.config["q"]))
            if queueInfo.status_code == 200:
                print("get info", queueInfo.text)
                rs = json.loads(queueInfo.text)["res"]
                if rs["messages_ready"] > 0 or rs["messages"] > 0:
                    self.ch.worker(self.worker, self.ch.queue)
                else:
                    print("No msg So push this msg")
                    self.syncSignal.emit(True)
            else:
                print("failed")
        except Exception as e:
            serviceUrl = "http://syncn.club:9759"

    def worker(self, ch, method, properties, msg):
        try:
            if properties.type == "cmd":
                if properties.headers.get('host') == Setting.syncn().config["id"]:
                    # if self.debug: print(msg, properties.headers.get('host'), Setting.syncn().config["id"])
                    print("is me!!!!! no exit!!!!")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                else:
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("Another Computer connected!!")
                    ch.close()
                    print("sync stop")
                    self.exitSignal.emit(True)
            else:
                DAO = NoteSql.DAO()
                print("start sync insert data")
                DAO.sync(json.loads(msg)["res"])
                print("end sync insert data")
                ch.cancel()
                ch.close()
                print("close channel")
        except Exception as e:
            self.ch.channel.cancel()
            self.ch.channel.close()
            self.ch.reopenChannel()
            print("worker, check this {0}".format(e))        

if __name__ == "__main__":
    th_mq = mqSendThread()
    th_mq.start()
    while 1:
        time.sleep(1)