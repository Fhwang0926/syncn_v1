# import sqlite3, pydash as _, uuid
# #windows RS4 under version location is C: \Users\Username\AppData\Roaming\Microsoft\Sticky Notes\StickyNotes.snt 

# class noteSql():
#     def __init__(self, fullPath):
#         self.path = ''
#         self.cursor = None
#         self.conn = None
#         self.build(fullPath)
#         pass

#     def read(self, chk=False):
#         col = "WindowPosition, Theme, Id, ParentId" if chk else "Text, WindowPosition, Theme"
#         rs = self.cursor.execute("SELECT " + col + " FROM Note")
#         rs_array = []
#         for row in rs:
#             rs_array.append(row)
#             if(chk): break
#         return self.convert(rs_array, chk)


#     def build(self, path):
#         self.path = path
#         self.conn = sqlite3.connect(path)
#         self.cursor = self.conn.cursor()
#         pass
        

#     def update(self):
#         # db.execute('update note set  = ? where t1 = ?', (row['i1'], row['t1']))
#         # db.commit()
#         pass

#     def convert(self, items, chk):
#         notes = {}
#         cnt = 1
#         i = None
#         for item in items:
#             if(chk):
#                 i = {str(cnt): { "WindowPosition": item[0], "Theme": item[1], "Id" : item[2], "ParentId" : item[3] }}
#             else:
#                 i = {str(cnt): { "Text": item[0], "WindowPosition": item[1], "Theme": item[2] }}
#             notes.update(i)
#             cnt+=1
#         return notes

#     def check(self):
#         return self.read(chk=True)

# section

# def main():
#     dao = noteSql(
#         "C:\\Users\\hdh09\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite")
#     print(dao.read())
    
# if __name__ == '__main__':
#     main()

# import os
# def detailSearch(root_path):
#     for (path, dirname, files) in os.walk(root_path):
#         for f in files:
#             fullPath = path + '/' + f

#             print(fullPath)

# search2(os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+"\AppData\Local\Packages")



# section test mq connection

# import pika
# import json
# from Lib import *

# class MQ():
#     def __init__(self):
#         with open("Setting.syncn", 'r') as configfile:
#             self.ServerData = json.load(configfile)
#         self.QueueName = self.ServerData['q']
#         self.Userid = self.ServerData['id']
#         self.Userpw = self.ServerData['pw']
#         self.RoutingKey = self.QueueName
#         # self.SqlObject = NoteSql.noteSql()
#         # self.SqlData = self.SqlObject.read()
#         self.Message = "WTF"
#         self.exchange = "msg"


#     def SendQueue(self):
#         self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
#         # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
#         self.SendConnection = pika.BlockingConnection(pika.URLParameters(self.url))
#         self.SendChannel = self.SendConnection.channel()
#         # self.SendChannel.queue_declare(queue=self.QueueName)
#         self.SendChannel.basic_publish(exchange=self.exchange,routing_key=self.RoutingKey,body=json.dumps(self.Message))

#         print(" [x] Sent %r" % self.Message)
#         self.SendConnection.close()



#     def ReceiveQueue(self):
#         self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
#         # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
#         self.ReceiveConnection = pika.BlockingConnection(pika.URLParameters(self.url))
#         self.ReceiveChannel = self.ReceiveConnection.channel()
#         # self.ReceiveChannel.queue_declare(queue=self.QueueName)


#         self.ReceiveChannel.basic_consume(self.callback, queue=self.QueueName, no_ack=True)

#         print(' [*] Wationg for messages. To exit press CTRL+C')
#         self.ReceiveChannel.start_consuming()

#     def callback(self, ch, method, properties, body):
#         print(" [x] Received %r" % json.loads(body))
#         #example = json.loads(body)['1']['Text']

# if __name__ == '__main__':
#     Connection = MQ()
#     Connection.SendQueue()
#     Connection.ReceiveQueue()


# #  section
# import sys
# from PyQt5.QtCore import QSize
# from PyQt5.QtGui import QImage, QPalette, QBrush
# from PyQt5.QtWidgets import *

# class MainWindow(QWidget):
#     def __init__(self):
#        QWidget.__init__(self)
#        self.setGeometry(100,100,300,200)

#        oImage = QImage("UI\\images\\bg.png")
#        sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
#        palette = QPalette()
#        palette.setBrush(10, QBrush(sImage))                     # 10 = Windowrole
#        self.setPalette(palette)

#        self.label = QLabel('Test', self)                        # test, if it's really backgroundimage
#        self.label.setGeometry(50,50,200,50)

#        self.show()

# if __name__ == "__main__":

#     app = QApplication(sys.argv)
#     oMainwindow = MainWindow()
#     sys.exit(app.exec_())
#########################################################
## customize Title bar
## dotpy.ir
## iraj.jelo@gmail.com
#########################################################
# import sys
# from PyQt5 import QtWidgets, QtGui
# from PyQt5 import QtCore
# from PyQt5.QtCore import Qt

# class TitleBar(QtWidgets.QDialog):
#     def __init__(self, parent=None):
#         QtWidgets.QWidget.__init__(self, parent)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         css = """
#         QWidget{
#             Background: #AA00AA;
#             color:white;
#             font:12px bold;
#             font-weight:bold;
#             border-radius: 1px;
#             height: 11px;
#         }
#         QDialog{
#             Background-image:url('img/titlebar bg.png');
#             font-size:12px;
#             color: black;

#         }
#         QToolButton{
#             Background:#AA00AA;
#             font-size:11px;
#         }
#         QToolButton:hover{
#             Background: #FF00FF;
#             font-size:11px;
#         }
#         """
#         self.setAutoFillBackground(True)
#         self.setBackgroundRole(QtGui.QPalette.Highlight)
#         self.setStyleSheet(css)
#         self.minimize=QtWidgets.QToolButton(self)
#         self.minimize.setIcon(QtGui.QIcon('img/min.png'))
#         self.maximize=QtWidgets.QToolButton(self)
#         self.maximize.setIcon(QtGui.QIcon('img/max.png'))
#         close=QtWidgets.QToolButton(self)
#         close.setIcon(QtGui.QIcon('img/close.png'))
#         self.minimize.setMinimumHeight(10)
#         close.setMinimumHeight(10)
#         self.maximize.setMinimumHeight(10)
#         label=QtWidgets.QLabel(self)
#         label.setText("test")
#         self.setWindowTitle("Window Title")
#         hbox=QtWidgets.QHBoxLayout(self)
#         hbox.addWidget(label)
#         hbox.addWidget(self.minimize)
#         hbox.addWidget(self.maximize)
#         hbox.addWidget(close)
#         hbox.insertStretch(1,500)
#         hbox.setSpacing(0)
#         self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
#         self.maxNormal=False
#         close.clicked.connect(self.close)
#         self.minimize.clicked.connect(self.showSmall)
#         self.maximize.clicked.connect(self.showMaxRestore)

#     def showSmall(self):
#         box.showMinimized()

#     def showMaxRestore(self):
#         if(self.maxNormal):
#             box.showNormal()
#             self.maxNormal= False
#             self.maximize.setIcon(QtGui.QIcon('img/max.png'))
#             print('1')
#         else:
#             box.showMaximized()
#             self.maxNormal=  True
#             print('2')
#             self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

#     def close(self):
#         box.close()

#     def mousePressEvent(self,event):
#         if event.button() == Qt.LeftButton:
#             box.moving = True
#             box.offset = event.pos()

#     def mouseMoveEvent(self,event):
#         if box.moving: box.move(event.globalPos()-box.offset)


# class Frame(QtWidgets.QFrame):
#     def __init__(self, parent=None):
#         QtWidgets.QFrame.__init__(self, parent)
#         self.m_mouse_down= False
#         self.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setMouseTracking(True)
#         self.m_titleBar= TitleBar(self)
#         self.m_content= QtWidgets.QWidget(self)
#         vbox=QtWidgets.QVBoxLayout(self)
#         vbox.addWidget(self.m_titleBar)
#         vbox.setContentsMargins(0, 0, 0, 0)
#         vbox.setSpacing(0)
#         layout=QtWidgets.QVBoxLayout()
#         layout.addWidget(self.m_content)
#         layout.setContentsMargins(5, 5, 5, 5)
#         layout.setSpacing(0)
#         vbox.addLayout(layout)
#         # Allows you to access the content area of the frame
#         # where widgets and layouts can be added

#     def contentWidget(self):
#         return self.m_content

#     def titleBar(self):
#         return self.m_titleBar

#     def mousePressEvent(self,event):
#         self.m_old_pos = event.pos()
#         self.m_mouse_down = event.button()== Qt.LeftButton

#     def mouseMoveEvent(self,event):
        
#         x=event.x()
#         y=event.y()
#         print(x, y)

#     def mouseReleaseEvent(self,event):
#         m_mouse_down=False

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     box = Frame()
#     box.move(60,60)
#     l=QtWidgets.QVBoxLayout(box.contentWidget())
#     l.setContentsMargins(0, 0, 0, 0)
#     edit=QtWidgets.QLabel("""I would've did anything for you to show you how much I adored you
# But it's over now, it's too late to save our loveJust promise me you'll think of me
# Every time you look up in the sky and see a star 'cuz I'm  your star.""")
#     l.addWidget(edit)
#     box.show()
#     app.exec_()
# section
#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
#         QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
#         QMessageBox, QMenu, QPushButton, QSpinBox, QStyle, QSystemTrayIcon,
#         QTextEdit, QVBoxLayout)

# import systray_rc


# class Window(QDialog):
#     def __init__(self):
#         super(Window, self).__init__()

#         self.createIconGroupBox()
#         self.createMessageGroupBox()

#         self.iconLabel.setMinimumWidth(self.durationLabel.sizeHint().width())

#         self.createActions()
#         self.createTrayIcon()

#         self.showMessageButton.clicked.connect(self.showMessage)
#         self.showIconCheckBox.toggled.connect(self.trayIcon.setVisible)
#         self.iconComboBox.currentIndexChanged.connect(self.setIcon)
#         self.trayIcon.messageClicked.connect(self.messageClicked)
#         self.trayIcon.activated.connect(self.iconActivated)

#         mainLayout = QVBoxLayout()
#         mainLayout.addWidget(self.iconGroupBox)
#         mainLayout.addWidget(self.messageGroupBox)
#         self.setLayout(mainLayout)

#         self.iconComboBox.setCurrentIndex(1)
#         self.trayIcon.show()

#         self.setWindowTitle("Systray")
#         self.resize(400, 300)

#     def setVisible(self, visible):
#         self.minimizeAction.setEnabled(visible)
#         self.maximizeAction.setEnabled(not self.isMaximized())
#         self.restoreAction.setEnabled(self.isMaximized() or not visible)
#         super(Window, self).setVisible(visible)

#     def closeEvent(self, event):
#         if self.trayIcon.isVisible():
#             QMessageBox.information(self, "Systray",
#                     "The program will keep running in the system tray. To "
#                     "terminate the program, choose <b>Quit</b> in the "
#                     "context menu of the system tray entry.")
#             self.hide()
#             event.ignore()

#     def setIcon(self, index):
#         icon = self.iconComboBox.itemIcon(index)
#         self.trayIcon.setIcon(icon)
#         self.setWindowIcon(icon)

#         self.trayIcon.setToolTip(self.iconComboBox.itemText(index))

#     def iconActivated(self, reason):
#         if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
#             self.iconComboBox.setCurrentIndex(
#                     (self.iconComboBox.currentIndex() + 1)
#                     % self.iconComboBox.count())
#         elif reason == QSystemTrayIcon.MiddleClick:
#             self.showMessage()

#     def showMessage(self):
#         icon = QSystemTrayIcon.MessageIcon(
#                 self.typeComboBox.itemData(self.typeComboBox.currentIndex()))
#         self.trayIcon.showMessage(self.titleEdit.text(),
#                 self.bodyEdit.toPlainText(), icon,
#                 self.durationSpinBox.value() * 1000)

#     def messageClicked(self):
#         QMessageBox.information(None, "Systray",
#                 "Sorry, I already gave what help I could.\nMaybe you should "
#                 "try asking a human?")

#     def createIconGroupBox(self):
#         self.iconGroupBox = QGroupBox("Tray Icon")

#         self.iconLabel = QLabel("Icon:")

#         self.iconComboBox = QComboBox()
#         self.iconComboBox.addItem(QIcon(':/images/bad.png'), "Bad")
#         self.iconComboBox.addItem(QIcon(':/images/heart.png'), "Heart")
#         self.iconComboBox.addItem(QIcon(':/images/trash.png'), "Trash")

#         self.showIconCheckBox = QCheckBox("Show icon")
#         self.showIconCheckBox.setChecked(True)

#         iconLayout = QHBoxLayout()
#         iconLayout.addWidget(self.iconLabel)
#         iconLayout.addWidget(self.iconComboBox)
#         iconLayout.addStretch()
#         iconLayout.addWidget(self.showIconCheckBox)
#         self.iconGroupBox.setLayout(iconLayout)

#     def createMessageGroupBox(self):
#         self.messageGroupBox = QGroupBox("Balloon Message")

#         typeLabel = QLabel("Type:")

#         self.typeComboBox = QComboBox()
#         self.typeComboBox.addItem("None", QSystemTrayIcon.NoIcon)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxInformation), "Information",
#                 QSystemTrayIcon.Information)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxWarning), "Warning",
#                 QSystemTrayIcon.Warning)
#         self.typeComboBox.addItem(self.style().standardIcon(
#                 QStyle.SP_MessageBoxCritical), "Critical",
#                 QSystemTrayIcon.Critical)
#         self.typeComboBox.setCurrentIndex(1)

#         self.durationLabel = QLabel("Duration:")

#         self.durationSpinBox = QSpinBox()
#         self.durationSpinBox.setRange(5, 60)
#         self.durationSpinBox.setSuffix(" s")
#         self.durationSpinBox.setValue(15)

#         durationWarningLabel = QLabel("(some systems might ignore this hint)")
#         durationWarningLabel.setIndent(10)

#         titleLabel = QLabel("Title:")

#         self.titleEdit = QLineEdit("Cannot connect to network")

#         bodyLabel = QLabel("Body:")

#         self.bodyEdit = QTextEdit()
#         self.bodyEdit.setPlainText("Don't believe me. Honestly, I don't have "
#                 "a clue.\nClick this balloon for details.")

#         self.showMessageButton = QPushButton("Show Message")
#         self.showMessageButton.setDefault(True)

#         messageLayout = QGridLayout()
#         messageLayout.addWidget(typeLabel, 0, 0)
#         messageLayout.addWidget(self.typeComboBox, 0, 1, 1, 2)
#         messageLayout.addWidget(self.durationLabel, 1, 0)
#         messageLayout.addWidget(self.durationSpinBox, 1, 1)
#         messageLayout.addWidget(durationWarningLabel, 1, 2, 1, 3)
#         messageLayout.addWidget(titleLabel, 2, 0)
#         messageLayout.addWidget(self.titleEdit, 2, 1, 1, 4)
#         messageLayout.addWidget(bodyLabel, 3, 0)
#         messageLayout.addWidget(self.bodyEdit, 3, 1, 2, 4)
#         messageLayout.addWidget(self.showMessageButton, 5, 4)
#         messageLayout.setColumnStretch(3, 1)
#         messageLayout.setRowStretch(4, 1)
#         self.messageGroupBox.setLayout(messageLayout)

#     def createActions(self):
#         self.minimizeAction = QAction("Mi&nimize", self, triggered=self.hide)
#         self.maximizeAction = QAction("Ma&ximize", self,
#                 triggered=self.showMaximized)
#         self.restoreAction = QAction("&Restore", self,
#                 triggered=self.showNormal)
#         self.quitAction = QAction("&Quit", self,
#                 triggered=QApplication.instance().quit)

#     def createTrayIcon(self):
#          self.trayIconMenu = QMenu(self)
#          self.trayIconMenu.addAction(self.minimizeAction)
#          self.trayIconMenu.addAction(self.maximizeAction)
#          self.trayIconMenu.addAction(self.restoreAction)
#          self.trayIconMenu.addSeparator()
#          self.trayIconMenu.addAction(self.quitAction)

#          self.trayIcon = QSystemTrayIcon(self)
#          self.trayIcon.setContextMenu(self.trayIconMenu)


# if __name__ == '__main__':

#     import sys
    

#     app = QApplication(sys.argv)

#     if not QSystemTrayIcon.isSystemTrayAvailable():
#         QMessageBox.critical(None, "Systray",
#                 "I couldn't detect any system tray on this system.")
#         sys.exit(1)

#     QApplication.setQuitOnLastWindowClosed(False)

#     window = Window()
#     window.show()
#     sys.exit(app.exec_())


# section

# icon_path="custom.ico"
# from win10toast import ToastNotifier
# import time
# toaster = ToastNotifier()
# toaster.show_toast("Hello World!!!", "Python is 10 seconds awsm!", duration=10)

# toaster.show_toast("Example two", "This notification is in it's own thread!", icon_path=None, duration=5, threaded=True)
# # Wait for threaded notification to finish
# while toaster.notification_active(): time.sleep(0.1)

# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# code source: https://stackoverflow.com/questions/893984/pyqt-show-menu-in-a-system-tray-application  - add answer PyQt5
#PyQt4 to PyQt5 version: https://stackoverflow.com/questions/20749819/pyqt5-failing-import-of-qtgui
# class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

#     def __init__(self, icon, parent=None):
#         QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
#         menu = QtWidgets.QMenu(parent)
#         syncAction = menu.addAction("Sync")
#         shareAction = menu.addAction("Share")
#         protectAction = menu.addAction("Encryption")
#         uninstallAction = menu.addAction("Uninstall")
#         logoutAction = menu.addAction("Logout")
#         exitAction = menu.addAction("Exit")
#         self.setContextMenu(menu)

# def main(image):
#     app = QtWidgets.QApplication(sys.argv)

#     w = QtWidgets.QWidget()
#     trayIcon = SystemTrayIcon(QtGui.QIcon(image), w)

#     trayIcon.show()
#     sys.exit(app.exec_())

# if __name__ == '__main__':
#     on=r'UI\\images\\sync.png'# ADD PATH OF YOUR ICON HERE .png works
#     main(on)