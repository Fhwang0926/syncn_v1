import Auth, Conf, MQ, Search, Setting
import json, itertools ,threading, pdb

class Control():
    def __init__(self, debug=True):
        # init
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.getSetting = Setting.DataSet(search=self.search, debug=debug)
        self.applySetting = Setting.DataApply(debug=debug)

        # Email auth
        # self.auth.build("wdt0818@naver.com")
        # self.auth.sendUrl()
        # time.sleep(15)
        # self.auth.getServerInfo()

        # Set the setting file data
        setFile = self.conf.read()
        self.mq.build(setFile)

        # Get xpad data
        self.sendData = self.getSetting.run()

        # Send and Receive message
        self.mq.connection()
        # self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        self.receiveData = json.loads(self.receiveData.decode())

        # Apply the data
        # pdb.set_trace()
        self.applySetting.dataParse(self.receiveData)
        self.applySetting.dataApply()

    def compareData(self):
        items = list(itertools.product(self.sendData, self.receiveData))
        fil = [i == j for (i,j) in items]
        filItem = list(itertools.compress(items, fil)) # filItem = list(set(self.sendData).intersection(self.receiveData))
        # true index = list(itertools.compress(range(len(fil)),fil))
        self.matchList = [k[0] for k in filItem]
        self.mismatchList = list(set(self.sendData + self.receiveData))
        for i in list(set(self.sendData + self.receiveData)):
            for j in self.matchList:
                if i == j:
                    self.mismatchList.remove(j)
                    break

if __name__ == '__main__':
    test = Control()
