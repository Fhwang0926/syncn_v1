try:
    from Lib import Setting, MQ, NoteSql, Search, Signal
except ImportError:
    print("import errer")
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
        self.target = Search.PathSearcher().run()
        self.signal = Signal.signal(debug=self.debug)
        self.signalRunner = self.signal.connect()

    def __del__(self):
        if self.debug: print(".... end thread.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

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
    reciveSignal = pyqtSignal(bool)
    def __init__(self, debug=False):
        super().__init__()
        try:
            self.debug = debug
            self.msg = ''
            self.DAO = NoteSql.DAO()
            
        except Exception as e:
            print("mqSendThread, check this {0}".format(e))

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

            # fix msg cnt
            queueInfo = requests.get(url="{0}/info/queue/{1}".format(ch.config["service"], ch.config["q"]))
            if queueInfo.status_code == 200:
                rs = json.loads(queueInfo.text)["res"]
                if rs["messages_ready"] > 0 or rs["messages"] > 1:
                    print("msg cnt fix just 1")
                    ch.worker(self.worker, ch.queue)
            else:
                print("failed")
            
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
        except Exception as e:
            print("mqReciveThread init, check this {0}".format(e))
            pass

    def __del__(self):
        print(".... mqReciveThread end.....")
        self.wait()
    
    def stop(self):
        self.isRun = False

    def run(self):
        self.isRun = True
        try:
            ch = MQ.MQ()
            queueInfo = requests.get(url="{0}/info/queue/{1}".format(ch.config["service"], ch.config["q"]))
            if queueInfo.status_code == 200:
                print("get info", queueInfo.text)
                rs = json.loads(queueInfo.text)["res"]
                if rs["messages_ready"] > 0 or rs["messages"] > 0:
                    ch.worker(self.worker, ch.queue, once=True)
                else:
                    print("No msg So push this msg")
                    self.syncSignal.emit(True)
            else:
                print("failed")
            
        except Exception as e:
            print("mqReciveThread run, check this {0}".format(e))
            

    def worker(self, ch, method, properties, msg, once=False):
        try:
            if properties.type == "cmd":
                if properties.headers.get('host') == Setting.syncn().config["id"]:
                    # if self.debug: print(msg, properties.headers.get('host'), Setting.syncn().config["id"])
                    print("is me!!!!! no exit!!!!")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                else:
                    print("Another Computer connected!!")
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("is not me!!!!! exit!!!!")
                    self.exitSignal.emit(True)
            else:
                DAO = NoteSql.DAO()
                print("start sync insert data")
                if DAO.sync(json.loads(msg)["res"])["res"]:
                    print("[+] OK - sync send mail")
                print("end sync insert data")

                if once:
                    ch.cancel()
                    ch.close()
                    print("end worker no ack so 1 msg in queue")
                    return
                else:
                    ch.basic_ack(delivery_tag = method.delivery_tag)
                    print("ack")
        except Exception as e:
            ch.channel.cancel()
            ch.channel.close()
            print("worker, check this {0}".format(e))        

if __name__ == "__main__":
    th_mq = mqSendThread()
    th_mq.start()
    while 1:
        time.sleep(1)