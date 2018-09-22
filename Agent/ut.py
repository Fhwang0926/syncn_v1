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
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class TitleBar(QtWidgets.QDialog):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        css = """
        QWidget{
            Background: #AA00AA;
            color:white;
            font:12px bold;
            font-weight:bold;
            border-radius: 1px;
            height: 11px;
        }
        QDialog{
            Background-image:url('img/titlebar bg.png');
            font-size:12px;
            color: black;

        }
        QToolButton{
            Background:#AA00AA;
            font-size:11px;
        }
        QToolButton:hover{
            Background: #FF00FF;
            font-size:11px;
        }
        """
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QtGui.QPalette.Highlight)
        self.setStyleSheet(css)
        self.minimize=QtWidgets.QToolButton(self)
        self.minimize.setIcon(QtGui.QIcon('img/min.png'))
        self.maximize=QtWidgets.QToolButton(self)
        self.maximize.setIcon(QtGui.QIcon('img/max.png'))
        close=QtWidgets.QToolButton(self)
        close.setIcon(QtGui.QIcon('img/close.png'))
        self.minimize.setMinimumHeight(10)
        close.setMinimumHeight(10)
        self.maximize.setMinimumHeight(10)
        label=QtWidgets.QLabel(self)
        label.setText("test")
        self.setWindowTitle("Window Title")
        hbox=QtWidgets.QHBoxLayout(self)
        hbox.addWidget(label)
        hbox.addWidget(self.minimize)
        hbox.addWidget(self.maximize)
        hbox.addWidget(close)
        hbox.insertStretch(1,500)
        hbox.setSpacing(0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.maxNormal=False
        close.clicked.connect(self.close)
        self.minimize.clicked.connect(self.showSmall)
        self.maximize.clicked.connect(self.showMaxRestore)

    def showSmall(self):
        box.showMinimized()

    def showMaxRestore(self):
        if(self.maxNormal):
            box.showNormal()
            self.maxNormal= False
            self.maximize.setIcon(QtGui.QIcon('img/max.png'))
            print('1')
        else:
            box.showMaximized()
            self.maxNormal=  True
            print('2')
            self.maximize.setIcon(QtGui.QIcon('img/max2.png'))

    def close(self):
        box.close()

    def mousePressEvent(self,event):
        if event.button() == Qt.LeftButton:
            box.moving = True
            box.offset = event.pos()

    def mouseMoveEvent(self,event):
        if box.moving: box.move(event.globalPos()-box.offset)


class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        QtWidgets.QFrame.__init__(self, parent)
        self.m_mouse_down= False
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.m_titleBar= TitleBar(self)
        self.m_content= QtWidgets.QWidget(self)
        vbox=QtWidgets.QVBoxLayout(self)
        vbox.addWidget(self.m_titleBar)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        layout=QtWidgets.QVBoxLayout()
        layout.addWidget(self.m_content)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        vbox.addLayout(layout)
        # Allows you to access the content area of the frame
        # where widgets and layouts can be added

    def contentWidget(self):
        return self.m_content

    def titleBar(self):
        return self.m_titleBar

    def mousePressEvent(self,event):
        self.m_old_pos = event.pos()
        self.m_mouse_down = event.button()== Qt.LeftButton

    def mouseMoveEvent(self,event):
        
        x=event.x()
        y=event.y()
        print(x, y)

    def mouseReleaseEvent(self,event):
        m_mouse_down=False

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    box = Frame()
    box.move(60,60)
    l=QtWidgets.QVBoxLayout(box.contentWidget())
    l.setContentsMargins(0, 0, 0, 0)
    edit=QtWidgets.QLabel("""I would've did anything for you to show you how much I adored you
But it's over now, it's too late to save our loveJust promise me you'll think of me
Every time you look up in the sky and see a star 'cuz I'm  your star.""")
    l.addWidget(edit)
    box.show()
    app.exec_()