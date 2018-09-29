from Lib import Core, UI, Setting, Auth, NoteSql
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import os
import requests
import json

class SyncN(object):
    def __init__(self):
        super().__init__()
        # init
        self.debug = True
        self.app = QtWidgets.QApplication(sys.argv)
        # init UI
        self.UI = UI.UI()
        if os.path.exists(Setting.syncn().path):
            self.UI.authStyle()
        #init auth
        self.OTP = Auth.EmailCert(debug=True)
        # init signal
        self.th_signal = Core.signalThread(debug=True)
        # init MQ
        self.th_mqSender = Core.mqSendThread(debug=True)
        # init MQ
        self.th_mqReciver = Core.mqReciveThread(debug=True)
        # init CMD
        self.th_cmd = Core.cmdThread(debug=True)
        # init mail
        # self.th_mail = Core.mailThread(debug=True)
        # init authTimer
        self.th_authTimer = Core.authTimer(debug=True)
        
        # init func
        self.connectInterface()
        
    
    def connectInterface(self):
        #define UI
        self.UI.tray.accountAction.triggered.connect(self.UI.windowTrigger)
        self.UI.tray.activated.connect(self.UI.openWindow)
        self.UI.tray.exitAction.triggered.connect(self.proExit)
        self.UI.input_info.textChanged.connect(self.UI.checkInput)
        self.UI.btn_close.clicked.connect(self.proExit)
        self.UI.btn_tray.clicked.connect(self.UI.windowTrigger)

        #define here
        self.UI.input_info.returnPressed.connect(self.proAuth)
        self.UI.btn_ok.clicked.connect(self.proAuth)
        self.UI.tray.logoutAction.triggered.connect(self.proLogout)
        if self.debug: print("[+] Registration Interface")

    def setThreadChannel(self):
        self.th_signal.syncSignal.connect(self.th_mqSender.start)
        self.th_mqReciver.exitSignal.connect(self.proExit)
        self.th_mqReciver.syncSignal.connect(self.th_mqSender.start)
        self.th_mqReciver.execSignal.connect(self.openNote)
        self.th_mqReciver.killSignal.connect(self.closeNote)
        self.th_cmd.exitSignal.connect(self.proExit)
        self.th_authTimer.authResetSignal.connect(self.authReset)
        self.th_authTimer.authTimerSignal.connect(lambda strTime:self.UI.l_info.setText("We Sended Auth mail\n{0}".format(strTime)))
    
    def authReset(self):
        self.OTP.buildClear()
        self.UI.l_info.setText("Typing Your E-mail")
        self.UI.l_info.setStyleSheet("color:black;\n")
        self.UI.btn_ok.setText("OK")
        self.OTP.isCreateOTP = False

    
    def proExit(self, code=0):
        if self.th_signal.isRunning(): self.th_cmd.terminate()
        if self.th_cmd.isRunning(): self.th_cmd.terminate()
        if self.th_mqSender.isRunning(): self.th_cmd.terminate()
        if self.th_mqReciver.isRunning(): self.th_cmd.terminate()
        self.UI.close()
        sys.exit(code)

    def run(self):
        self.closeNote()
        self.setThreadChannel()
        if self.UI.auth:
            self.disconnectCMD()
            self.th_mqReciver.once = True
            self.th_mqReciver.start()
            self.th_signal.start()
        self.UI.show()
        if self.UI.auth:
            self.UI.windowTrigger()
        self.proExit(self.app.exec_())
    
    def proAuth(self):
        if self.UI.auth: return self.UI.windowTrigger()
        if not self.OTP.isCreateOTP:
            # need create OTP
            if not self.OTP.build(self.UI.input_info.text(), "syncn.club:9759"):
                self.UI.l_info.setText("Check Email Address\n%")
                self.UI.l_info.setStyleSheet("color:red;\n")
                return
            else:
                if self.OTP.createOTP():
                    self.UI.l_info.setStyleSheet("color:green;\n")
                    self.UI.l_info.setText("We Sended Auth mail")
                    self.UI.btn_ok.setText("Auth OK ?")
                    self.th_authTimer.start()
                else:
                    self.UI.l_info.setStyleSheet("color:red;")
                    self.UI.l_info.setText("Failed send Auth email")
        else:
            # need auth OTP
            if self.OTP.authOTP():
                self.UI.authStyle()
                self.disconnectCMD()
                self.th_mqReciver.once = True
                self.th_mqReciver.start()
                self.th_signal.start()
            else:
                self.UI.l_info.setStyleSheet("color:red;\n")
                self.UI.l_info.setText("Auth Failed, see email")
    
    def openNote(self):
        os.system("explorer.exe shell:appsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App")
    
    def closeNote(self):
        os.system('taskkill /f /im Microsoft.Notes.exe')

    def proLogout(self):
        try:
            os.remove(self.UI.syncn["config"])
        except Exception as e:
            print("{0} proLogout, check this {0}".format(__file__, e))
        finally:
            sys.exit(0)

    # excute others agent disconnect all then only connect me
    def disconnectCMD(self):
        try:
            self.th_mqSender.type = "cmd"
            self.th_mqSender.start()
            self.th_cmd.start()
            # config = Setting.syncn().config
            # consumerInfo = requests.get(url="{0}/info/queue/{1}".format(config["service"], config["q"]))
            # if consumerInfo.status_code == 200:
            #     print("check info", json.loads(consumerInfo.text)["res"])
            #     rs = json.loads(consumerInfo.text)["res"]["consumer"]
            #     if not rs: print("Non running agent")
            #     for x in range(0, rs):
            #         print("send exit cmd", x)
            #         self.th_mqSender.msg = "quit" # all client remove
            #         self.th_mqSender.start()
            #         self.th_mqSender.wait() # all client remove end
            #         time.sleep(1)
            # else:
            #     print("check consumers failed")
            #     if self.debug: print(json.loads(consumerInfo.text)['e'])
            print(".")
        except Exception as e:
            print("{0} disconnectCMD, check this {1}".format(__file__, e))
            pass

if __name__ == '__main__':
    main = SyncN()
    main.run()