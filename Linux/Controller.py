import Auth, Conf, MQ, Search, Setting, Observer
import json, itertools ,threading, pdb, time
from PyQt5.QtCore import QThread

class Control():
    def __init__(self, debug=True):
        # init
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.getSetting = Setting.DataSet(search=self.search, debug=debug)
        self.applySetting = Setting.DataApply(debug=debug)

        # set
        self.setFile = self.conf.read()
        self.mq.build(self.setFile)
        self.sendData = self.getSetting.run()
        self.mq.connection()

    def run(self):
        # Set the setting file data
        self.setFile = self.conf.read()
        self.mq.build(self.setFile)

        # Get xpad data
        self.sendData = self.getSetting.run()

        # Receive message because of data comparing
        self.mq.connection()
        # self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if self.receiveData:
            self.receiveData = json.loads(self.receiveData.decode())
        else:
            print("No message in the queue")
            return

        # Compare between server data and local data
        self.compareData()
        print("origin: ",len(self.sendData))

        # Add the new data and Send the message to MQ server
        self.sendData.update(self.receiveData)
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        print("added: ",len(self.sendData))

        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=False)
        self.receiveData = json.loads(self.receiveData.decode())
        # Apply the data
        # pdb.set_trace()
        self.applySetting.dataParse(self.receiveData)
        self.applySetting.dataApply()

    # New user access
    def firstLogin(self):
        self.sendData = self.getSetting.run()
        self.mq.connection()

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
    def __init__(self,search, debug=True):
        super().__init__()
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        self.observer = Observer.Observer(path="/Users/jeoninsuck/test.rtf", debug=self.debug)
        self.is_run = False
        self.is_send = False

    def run(self):
        try:
            self.is_run = True
            self.observer.start()
            while True:
                if self.observer.send_signal == True:
                    if self.debug: print("Get the Signal\n")
                    self.observer.send_signal = False
        except Exception as e:
            print("signalTread run() method error, message: {0}\n".format(e))

if __name__ == '__main__':
    test = Control()
    sig = signalThread(search='')
    sig.run()
    #test.run()
