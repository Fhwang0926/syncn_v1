import Auth, Conf, MQ, Search, Setting, Observer, NoteSql
import json, itertools, pdb, time, sys, os
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *

class Control(QWidget):
    def __init__(self, debug=True):
        # super().__init__()
        # init
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.xpadGet= Setting.DataSet(search=self.search, debug=debug)
        self.xpadApply= Setting.DataApply(debug=debug)
        self.sticyOb = NoteSql.DAO(fullpath=self.search.fileSearch(file="plum", detailPath=os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'])[0], debug=debug )

        # set
        self.setFile = self.conf.read()
        self.mq.build(self.setFile)
        self.mq.connection()

    def run(self):
        oscheck = sys.platform
        if oscheck == "linux" or oscheck == "linux2":
            self.linuxFirst()
# signal 받아서 동기화 과정 들어가야 됨
        elif oscheck == "win32":
            self.windowFirst()


    def sync(self):
        self.sendData = self.xpadGet.run()
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if self.receiveData:
            self.receiveData = json.loads(self.receiveData.decode())
        else:
            print("No message in the queue")
            return
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))

    # 기존 메세지랑 비교하는거 아직 적용 안함
    # New user access window version
    def windowFirst(self):
        # Set the setting file data
        setFile = self.conf.read()
        # if new user, email auth first
        if setFile == False:
            self.emailAuth()
        self.mq.build(setFile)
        sendData = self.sticyOb.read()
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(sendData))
        receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if receiveData:
            receiveData = json.loads(receiveData.decode())
        else:
            print("No message in the queue")
            return

    # New user access linux version
    def linuxFirst(self):
        # Set the setting file data
        self.setFile = self.conf.read()
        # if new user, email auth first
        if self.setFile == False:
            self.emailAuth()
        self.mq.build(self.setFile)
        # Get xpad data
        self.sendData = self.xpadGet.run()
        # Receive message because of data comparing
        # self.mq.connection()
        # self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if self.receiveData:
            self.receiveData = json.loads(self.receiveData.decode())
        else:
            print("No message in the queue")
            return
        # Compare between server data and local data
        self.compareData()
        # Add the new data and Send the message to MQ server
        self.sendData.update(self.receiveData)
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=False)
        self.receiveData = json.loads(self.receiveData.decode())
        # Apply the data
        self.xpadApply.dataParse(self.receiveData)
        self.xpadApply.dataApply()

    # Email auth
    def emailAuth(self):
        self.auth.build("wdt0818@naver.com")
        self.auth.sendUrl()
        time.sleep(15)
        self.auth.getServerInfo()

    def compareData(self):
        # items = list(itertools.product(self.sendData, self.receiveData))
        # fil = [i == j for (i,j) in items]
        # filItem = list(itertools.compress(items, fil))
        # true index = list(itertools.compress(range(len(fil)),fil))
        # self.matchList = [k[0] for k in filItem]
        # self.mismatchList = list(set(self.sendData + self.receiveData))
        # for i in list(set(self.sendData + self.receiveData)):
        #     for j in self.matchList:
        #         if i == j:
        #             self.mismatchList.remove(j)
        #             break
        self.matchList = list(set(self.sendData).intersection(self.receiveData))
        self.mismatchList = list(set(self.sendData)^set(self.receiveData))
        if self.debug:
            print("mathList: {0}".format(self.matchList))
            print("mismathList: {0}\n".format(self.mismatchList))

class signalThread(QThread):
    sendSignal = pyqtSignal(bool)
    def __init__(self,search, debug=True):
        super().__init__()
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        # self.observer = Observer.Observer(path=self.search, debug=self.debug)
        self.is_run = False
        self.is_send = False

    def run(self):
        try:
            test = Control()
            self.is_run = True
            self.observer.start()
            while True:
                if self.observer.send_signal == True:
                    if self.debug: print("Get the Signal\n")
                    # test.sync()
                    self.sendSignal(True)
                    self.observer.send_signal = False
        except Exception as e:
            print("signalTread run() method error, message: {0}\n".format(e))

if __name__ == '__main__':
    test = Control()
    # sig = signalThread(search='')
    # sig.run()
    test.run()
