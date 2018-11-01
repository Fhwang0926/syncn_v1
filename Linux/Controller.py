import Auth, Conf, MQ, Search, Setting
import time

class Control():
    def __init__(self, debug=True):
        # init
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.setting = Setting.DataSet(search=self.search, debug=debug)

        # Email auth
        # self.auth.build("wdt0818@naver.com")
        # self.auth.sendUrl()
        # time.sleep(15)
        # self.auth.getServerInfo()

        # Set the setting file data
        setFile = self.conf.read()
        self.mq.build(setFile)
        self.result = self.setting.run()
        self.mq.run(msg=self.result)




if __name__ == '__main__':
    test = Control()