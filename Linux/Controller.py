import Auth, Conf, MQ, Search, Setting
import json, threading

class Control():
    def __init__(self, debug=True):
        # init
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.getSetting = Setting.DataSet(search=self.search, debug=debug)
        self.applySetting = Setting.DataApply()

        # Email auth
        # self.auth.build("wdt0818@naver.com")
        # self.auth.sendUrl()
        # time.sleep(15)
        # self.auth.getServerInfo()

        # Set the setting file data
        setFile = self.conf.read()
        self.mq.build(setFile)

        # Get xpad data
        self.result = self.setting.run()

        # Send and Receive message
        self.mq.connection()
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.result))
        self.mq.receiveMsg(queue=self.mq.queue)




if __name__ == '__main__':
    test = Control()