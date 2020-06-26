from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import uic, QtGui, QtWidgets
import sys, os, pdb
import Controller

form_class = uic.loadUiType("SyncN.ui")[0]

class Xpad(QMainWindow, form_class):
    syncSignal = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.debug = True
        self.setupUi(self)
        self.th_control = Controller.Control()
        if sys.platform == "win32":
            self.th_stickySync = Controller.sticySignal(debug=self.debug)
            self.th_stickySync.syncSignal.connect(self.startSync)
        elif sys.platform == "linux" or sys.platform == "linux2":
            self.th_xpadSync = Controller.xpadSignal()
            self.th_xpadSync.sendSignal.connect(self.startSync)
        self.btn_ok.clicked.connect(self.emailAuth)
        self.is_sendEmail = False
        self.is_confirmEmail = False
        self.run()

    def run(self):
        #pdb.set_trace()
        if self.th_control.settingFileCheck():
            self.is_sendEmail = True
            self.is_confirmEmail = True
            self.authOk()
            self.th_control.start()
            if sys.platform == "win32":
                self.th_stickySync.start()
            elif sys.platform == "linux" or sys.platform == "linux2":
                self.th_xpadSync.start()
    def startSync(self):
        self.th_control.sync()

    def emailAuth(self):
        if not self.is_sendEmail:
            if self.th_control.emailSend(email=self.input_info.text()):
                self.l_info.setStyleSheet("color:green;\n")
                self.l_info.setText("We Sended Auth mail")
                self.btn_ok.setText("Auth OK ?")
                self.is_sendEmail = True
            else:
                self.l_info.setText("Check Email Address\n%")
                self.l_info.setStyleSheet("color:red;\n")
        else:
            if not self.is_confirmEmail:
                if self.th_control.emailconfirm():
                    self.authOk()
                    self.is_confirmEmail = True
                else:
                    self.l_info.setStyleSheet("color:red;\n")
                    self.l_info.setText("Auth Failed, see email")
            else:
                pass

    def authOk(self):
        self.l_info.setStyleSheet("color:green")
        self.l_info.setText("Successful Auth\nStart! SyncN on Tray")
        self.input_info.setAlignment(Qt.AlignCenter)
        self.input_info.setFont(QtGui.QFont("Corbel", 7, 10))
        self.input_info.setText("01234567890123")
        self.input_info.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_info.setEnabled(False)
        self.input_info.setClearButtonEnabled(False)
        self.btn_ok.setText("Run on Tray")
        self.btn_ok.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = Xpad()
    myWindow.show()
    app.exec_()
