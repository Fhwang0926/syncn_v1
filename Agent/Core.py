from Lib import Auth, UI, Setting, MQ, NoteSql

class SyncN(object):
    def __init__(self):
        self.UI.btn_ok.clicked.connect(self.procAuth)
        self.OTP = Auth().EmailCert()

    def run(self):
        pass

    def procAuth(self):
        print("WTF")
        # self.OTP.build()
        # if(self.OTP.isCreateOTP):
        #     client.createOTP()
        # else:
        #     client.authOTP()

if __name__ == '__main__':
    SyncN()
    