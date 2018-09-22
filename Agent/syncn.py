#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com
# comment format like html

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from Lib import Auth, Setting
from Core import *
import sys, os


class UI(QMainWindow):
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)

        super().__init__()
        self.debug = True
        self.auth = os.path.exists("setting.syncn")
        self.syncn = {
                "icon" : "UI/images/sync.ico",
                "trayicon" : "UI/images/sync.png",
                "config" : "setting.syncn"
        }
        self.setObjectName("MainWindow")
        self.OTP = Auth.EmailCert()

        # icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.syncn["icon"]), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        # tray self.syncn["trayicon"]
        self.tray = syncNTray(icon)
        
        # tray function
        self.tray.exitAction.triggered.connect(self.proExit)
        self.tray.protectAction.triggered.connect(self.encryptTrigger)
        self.tray.accountAction.triggered.connect(self.windowTrigger)
        self.tray.logoutAction.triggered.connect(self.proLogout)
        self.tray.activated.connect(self.openWindow)
        
        # window
        self.setWindowIcon(icon)
        self.setEnabled(True)
        self.resize(390, 590)
        self.setMinimumSize(QtCore.QSize(390, 590))
        self.setMouseTracking(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle("SyncN")        
        self.setStyleSheet("background-color:rgb(255, 255, 127);")

        # window - widget
        self.w_main = QtWidgets.QWidget(self)
        self.w_main.setStyleSheet("#btn_close:hover { color:black; }\n#btn_close { color:gray; }\n#btn_tray:hover { color:black; }\n#btn_tray { color:gray; }")
        self.w_main.setObjectName("w_main")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.w_main)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # window - widget - button
        self.btn_tray = QtWidgets.QPushButton(self.w_main)
        self.btn_tray.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_tray.setFont(QtGui.QFont("Corbel", 30, 80))
        self.btn_tray.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_tray.setStyleSheet("background-color:rgb(255, 255, 127);\nborder-style:none;\nfont-family:Corbel;\nfont-size:12px;\nfont-weight:900;")
        self.btn_tray.setObjectName("btn_tray")
        self.btn_tray.clicked.connect(self.windowTrigger)

        self.btn_close = QtWidgets.QPushButton(self.w_main)
        self.btn_close.setMinimumSize(QtCore.QSize(30, 30))
        self.btn_close.setFont(QtGui.QFont("Corbel", 12, 80))
        self.btn_close.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_close.setStyleSheet("background-color:rgb(255, 255, 127);\nborder-style:none;")
        self.btn_close.setObjectName("btn_close")
        self.btn_close.clicked.connect(self.proExit)

        self.btn_ok = QtWidgets.QPushButton(self.w_main)
        self.btn_ok.setEnabled(False)
        self.btn_ok.setMinimumSize(QtCore.QSize(280, 45))
        self.btn_ok.setFont(QtGui.QFont("Bahnschrift Condensed", 18, 50))
        self.btn_ok.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_ok.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.btn_ok.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.btn_ok.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_ok.setStyleSheet("background-color:rgb(246, 246, 246);\nborder-style:solid;\nborder-color:#e5d32e;\nborder-width:1px;")
        self.btn_ok.setInputMethodHints(QtCore.Qt.ImhNone)
        self.btn_ok.setObjectName("btn_ok")
        self.btn_ok.clicked.connect(self.proAuth)

        # window - widget - label
        self.l_title = QtWidgets.QLabel(self.w_main)
        self.l_title.setFont(QtGui.QFont("Bahnschrift Condensed", 52, 80))
        self.l_title.setStyleSheet("color:rgb(66, 54, 48)")
        self.l_title.setObjectName("l_title")
        self.l_info = QtWidgets.QLabel(self.w_main)
        self.l_info.setFont(QtGui.QFont("Bahnschrift SemiBold", 16, 80))
        self.l_info.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.l_info.setTextFormat(QtCore.Qt.PlainText)
        self.l_info.setAlignment(QtCore.Qt.AlignCenter)
        self.l_info.setObjectName("l_info")

        # window - widget - input
        self.input_info = QtWidgets.QLineEdit(self.w_main)
        self.input_info.setMinimumSize(QtCore.QSize(280, 45))
        self.input_info.setMaximumSize(QtCore.QSize(280, 45))
        self.input_info.setBaseSize(QtCore.QSize(280, 45))
        self.input_info.setFont(QtGui.QFont("Bahnschrift Condensed", 14))
        self.input_info.setStyleSheet("background-color:rgb(255, 255, 255);\nborder-style:solid;\nborder-color:#e5d32e;\nborder-width:1px;")
        self.input_info.setClearButtonEnabled(True)
        self.input_info.textChanged.connect(self.checkInput)
        self.input_info.setObjectName("input_info")
        self.input_info.returnPressed.connect(self.proAuth)

        # window - widget - spacer
        spacerItem = QtWidgets.QSpacerItem(500, 10, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        spacerItem4 = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        #layout - header
        self.la_header = QtWidgets.QHBoxLayout()
        self.la_header.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.la_header.setSpacing(2)
        self.la_header.addItem(spacerItem)
        self.la_header.addWidget(self.btn_tray)
        self.la_header.addWidget(self.btn_close)
        self.la_header.setObjectName("la_header")
        #layout - title
        self.la_body_all = QtWidgets.QHBoxLayout()
        self.la_body_all.addItem(spacerItem1)
        self.la_body_all.addWidget(self.l_title)
        self.la_body_all.addItem(spacerItem2)
        self.la_body_all.setObjectName("la_body_all")
        #layout - content
        self.la_footer_body = QtWidgets.QVBoxLayout()
        self.la_footer_body.addWidget(self.l_info)
        self.la_footer_body.addWidget(self.input_info)
        self.la_footer_body.addWidget(self.btn_ok)
        self.la_footer_body.addItem(spacerItem4)
        self.la_footer_body.setObjectName("la_footer_body")
        #layout - body
        self.la_footer_all = QtWidgets.QHBoxLayout()
        self.la_footer_all.addItem(spacerItem3)
        self.la_footer_all.addLayout(self.la_footer_body)
        self.la_footer_all.addItem(spacerItem5)
        self.la_footer_all.setObjectName("la_footer_all")
        #layout - html
        self.la_content = QtWidgets.QVBoxLayout()
        self.la_content.addLayout(self.la_body_all)
        self.la_content.addLayout(self.la_footer_all)
        self.la_content.setObjectName("la_content")
        
        self.verticalLayout_3.addLayout(self.la_header)
        self.verticalLayout_3.addLayout(self.la_content)
        self.setCentralWidget(self.w_main)
        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        # init thread
        self.th_mq = mqSendThread()
        self.th_signal = signalThread()
        self.th_signal.sync.connect(self.th_mq.run)
        

        # check auth
        if self.auth: self.authStyle()
        if self.debug: print("init End")
        self.show()
        sys.exit(app.exec_())

    # function
    def proExit(self):
        self.close()
        sys.exit(0)

    def checkInput(self, to):
        if self.input_info.text():
            self.btn_ok.setEnabled(True)
        else:
            self.btn_ok.setEnabled(False)

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()
        self.mouse_down = event.button()== Qt.LeftButton

    def mouseReleaseEvent(self, e):
        self.mouse_down = False

    def keyPressEvent(self, e):
        if e.key() == 16777216: self.windowTrigger()
        
    def mouseMoveEvent(self, event):
        x=event.x()
        y=event.y()
        self.move(self.pos() + event.globalPos() - self.old_pos)
        self.old_pos = event.globalPos()
        event.accept()
    
    def windowTrigger(self):
        if self.tray.isActive:
            self.show()
            self.tray.hide()
            self.tray.isActive = False
        else:
            self.hide()
            self.tray.show()
            self.tray.isActive = True
            self.sycnN(True)
    
    def sycnN(self, type):
        if type:
            # if (not self.th_mq.isRun) and self.auth: self.th_mq.start(self.config)
            if (not self.th_signal.isRun) and self.auth: self.th_signal.start()
        else:
            if self.th_mq.isRun: self.th_mq.stop()
            if self.th_signal.isRun: self.th_signal.stop()
        
            

    def encryptTrigger(self):
        self.tray.protectAction.checkable = True if self.tray.isEncrypt else False

    def test(self):
        print("test")
        self.tray.showMessage("Notify", "Hello")
    
    def proAuth(self):
        if self.auth: return self.windowTrigger()
        if not self.OTP.isCreateOTP:
            # need create OTP
            if not self.OTP.build(self.input_info.text(), "syncn.club:9759"):
                self.l_info.setText("Check Email Address")
                self.l_info.setStyleSheet("color:red;\n")
                return
            else:
                if self.OTP.createOTP():
                    self.l_info.setStyleSheet("color:green;\n")
                    self.l_info.setText("We Sended Auth mail")
                else:
                    self.l_info.setStyleSheet("color:red;\n")
                    self.l_info.setText("Failed send Auth email")
        else:
            # need auth OTP
            if self.OTP.authOTP():
                self.authStyle()
            else:
                self.l_info.setStyleSheet("color:red;\n")
                self.l_info.setText("Auth Failed, Check Email")
    
    def proLogout(self):
        try:
            os.remove(self.syncn["config"])
            sys.exit(0)
        except Exception as e:
            print(e)
            pass

    def authStyle(self):
        self.l_info.setStyleSheet("color:green;\n")
        self.l_info.setText("Successful Auth\nStart! SyncN on Tray")
        self.input_info.setAlignment(Qt.AlignCenter)
        self.input_info.setFont(QtGui.QFont("Corbel", 7, 10))
        self.input_info.setText("01234567890123")
        self.input_info.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_info.setEnabled(False)
        self.input_info.setClearButtonEnabled(False)
        self.btn_ok.setText("Run on Tray")
        self.auth = True
    
    def openWindow(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            self.windowTrigger()
            self.raise_()

    # QMessageBox.about(None, "Notify", "try check email address detail", )
    # self.msg("Notify", "Try Check Email Address Correctly")
    def msg(self, title, body):
        msg = QMessageBox()
        msg.setIcon(QtGui.QIcon(self.syncn["trayicon"])) 
        msg.setWindowTitle(title)
        msg.setText(body)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.w_main.setToolTip(_translate("MainWindow", "Sync your sticky note on Windows 10"))
        self.btn_tray.setToolTip(_translate("MainWindow", "Minimumrize window(Tray)"))
        self.btn_tray.setText(_translate("MainWindow", "_"))
        self.btn_close.setToolTip(_translate("MainWindow", "Close"))
        self.btn_close.setText(_translate("MainWindow", "X"))
        self.l_title.setText(_translate("MainWindow", "SyncN"))
        self.l_info.setText(_translate("MainWindow", "Typing Your E-mail"))
        self.input_info.setToolTip(_translate("MainWindow", "Using only your E-mail"))
        self.input_info.setPlaceholderText(_translate("MainWindow", "exampel@mail.com"))
        self.btn_ok.setToolTip(_translate("MainWindow", "Click when you sure Okay"))
        self.btn_ok.setText(_translate("MainWindow", "OK"))

class syncNTray(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        menu = QtWidgets.QMenu(parent)
        
        self.isEncrypt = False
        self.isActive = False
        self.syncAction = QtWidgets.QAction("Sync", self, checkable=True)
        self.syncAction.setStatusTip('Default Yes')
        self.syncAction.setChecked(False)
        menu.addAction(self.syncAction)
        self.shareAction = menu.addAction("Share")
        self.protectAction = QtWidgets.QAction("Encryption", self, checkable=True)
        self.protectAction.setStatusTip('Default No')
        self.protectAction.setChecked(False)
        menu.addAction(self.protectAction)
        self.accountAction = menu.addAction("Account")
        self.logoutAction = menu.addAction("Logout")
        self.exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        self.setToolTip("SyncN[:Sync Note on Windows]!")
        
if __name__ == "__main__":
    print("Start application")
    app = QtWidgets.QApplication(sys.argv)
    application = UI()
    

