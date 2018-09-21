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