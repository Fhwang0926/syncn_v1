import Auth, Conf, MQ, Search, Setting, Observer, NoteSql, Signal
import json, pdb, time, sys, os, subprocess
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *

class Control(QThread):
    def __init__(self, debug=True):
        super().__init__()
        # init
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        self.auth = Auth.EmailCert(debug=debug)
        self.conf = Conf.Conf(search=self.search,debug=debug)
        self.mq = MQ.MQ(debug=debug)
        self.xpadGet= Setting.DataSet(search=self.search, debug=debug)
        self.xpadApply= Setting.DataApply(debug=debug)
        if sys.platform == "win32": self.sticyOb = NoteSql.DAO(fullpath=self.search.fileSearch(file="plum", detailPath=os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'])[0], debug=debug)
        self.parser = Setting.DataParse(debug=debug)



    def run(self):
        # set
        self.setFile = self.conf.read()
        self.mq.build(self.setFile['res'])
        self.mq.connection()

        oscheck = sys.platform
        if oscheck == "linux" or oscheck == "linux2":
            self.linuxFirst()
# signal 받아서 동기화 과정 들어가야 됨
        elif oscheck == "win32":
            self.windowFirst()

    # if receive the signal, start to sync
    def sync(self):
        if sys.platform == "linux" or sys.platform == "linux2":
            self.sendData = self.xpadGet.run()
        elif sys.platform == "win32":
            self.sendData = self.sticyOb.read()
        oldData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        oldData = json.loads(oldData.decode())
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))

    # 기존 메세지랑 비교하는거 아직 적용 안함
    # New user access window version
    def windowFirst(self):
        # Set the setting file data
        setFile = self.conf.read()
        # if new user, email auth first
        if setFile == False:
            self.emailAuth()
        self.mq.build(setFile)
        sendData = self.sticyOb.read()
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(sendData))
        receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if receiveData:
            receiveData = json.loads(receiveData.decode())
        else:
            print("No message in the queue")
            return
        receiveData = self.parser.run(data=receiveData)
        self.sticyOb.sync(notes=receiveData['res'])
        self.closeSticy()
        self.openSticy()

    # New user access linux version
    def linuxFirst(self):
        # Set the setting file data
        self.setFile = self.conf.read()
        # if new user, email auth first
        if self.setFile == False:
            self.emailAuth()
        self.mq.build(self.setFile['res'])
        # Get xpad data
        self.sendData = self.xpadGet.run()
        # Receive message because of data comparing
        # self.mq.connection()
        # self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        if self.receiveData:
            self.receiveData = json.loads(self.receiveData.decode())
        else:
            print("No message in the queue")
            return
        self.receiveData = self.parser.run(data=self.receiveData)
        # Compare between server data and local data
        self.compareData()
        # Add the new data and Send the message to MQ server
        self.sendData.update(self.receiveData)
        self.mq.sendMsg(exchange="msg", routing_key=self.mq.queue, msg=json.dumps(self.sendData))
        self.receiveData = self.mq.receiveMsg(queue=self.mq.queue, ack=True)
        self.receiveData = json.loads(self.receiveData.decode())
        # Apply the data
        self.xpadApply.dataParse(self.receiveData)
        self.xpadApply.resetDir()
        self.xpadApply.dataApply()
        self.closeXpad()
        self.openXpad()

    # Email auth
    def settingFileCheck(self):
        if self.search.fileSearch(file="setting", extension="syncn", detailPath=os.path.abspath(__file__ + "/../../")):
            return True
        else:
            return False

    def emailSend(self, email):
        if self.auth.build(email):
            self.auth.sendUrl()
            return True
        return False

    def emailconfirm(self):
        if self.auth.getServerInfo():
            serverData = self.auth.getServerInfo()
            self.conf.write(serverData)
            return True
        return False

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

    def openSticy(self):
        subprocess.call("explorer.exe shell:appsFolder\Microsoft.MicrosoftStickyNotes_{0}!App".format('8wekyb3d8bbwe'),
                        creationflags=0x08000000)

    def closeSticy(self):
        subprocess.call('taskkill /f /im Microsoft.Notes.exe', creationflags=0x08000000)
        subprocess.call('taskkill /f /im Microsoft.StickyNotes.exe', creationflags=0x08000000)

    def openXpad(self):
        subprocess.call("xpad &", shell=True)

    def closeXpad(self):
        subprocess.call("pkill -9 -ef xpad",shell=True)

class xpadSignal(QThread):
    sendSignal = pyqtSignal(bool)
    def __init__(self, debug=True):
        super().__init__()
        self.debug = debug
        self.search = Search.PathSearch(debug=debug)
        self.observer = Observer.Observer(path=self.search, debug=self.debug)
        self.is_run = False
        self.is_send = False

    def run(self):
        try:
            test = Control()
            self.is_run = True
            self.observer.start()
            while True:
                if self.observer.send_signal == True:
                    if self.debug: print("Get the Signal\n")
                    # test.sync()
                    self.sendSignal.emit(True)
                    self.observer.send_signal = False
        except Exception as e:
            print("xpadSignal thread run() method error, message: {0}\n".format(e))


class sticySignal(QThread):
    syncSignal = pyqtSignal(bool)

    def __init__(self, debug=False):
        super().__init__()
        self.isRun = False
        self.debug = debug
        self.target = Search.PathSearch().fileSearch(file="plum", detailPath=os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'])[0]
        self.signal = Signal.signal(target=self.target, debug=self.debug)
        # self.signalRunner = self.signal.connect()

    def __del__(self):
        if self.debug: print(".... signalThread end.....")
        self.wait()

    def stop(self):
        self.isRun = False
        self.signal.disconnect()

    def run(self):
        self.signalRunner = self.signal.connect()
        try:
            self.isRun = next(self.signalRunner)
            while self.isRun:
                if self.debug: print("get send signal from sticky note")
                pdb.set_trace()
                self.syncSignal.emit(True)
                self.signalRunner.send(0)
                time.sleep(1)
        except Exception as e:
            self.stop()
            print("signalThread, check this {0}".format(e))


if __name__ == '__main__':
    # test = Control()
    sig = xpadSignal()
    sig.run()
    # test.emailAuth()
    #test.emailAuth()
    #test = sticySignal(target="C:\\Users\\jis\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite", debug=True)
    #test.run()
