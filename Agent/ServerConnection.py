import pika
import json
from Lib import *

class MQ():
    def __init__(self):
        with open("Setting.syncn", 'r') as configfile:
            self.ServerData = json.load(configfile)
        self.QueueName = self.ServerData['q']
        self.Userid = self.ServerData['id']
        self.Userpw = self.ServerData['pw']
        self.RoutingKey = self.QueueName
        # self.SqlObject = NoteSql.noteSql()
        # self.SqlData = self.SqlObject.read()
        self.Message = "WTF"
        self.exchange = "msg"


    def SendQueue(self):
        self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
        # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
        self.SendConnection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.SendChannel = self.SendConnection.channel()
        # self.SendChannel.queue_declare(queue=self.QueueName)
        self.SendChannel.basic_publish(exchange=self.exchange,routing_key=self.RoutingKey,body=json.dumps(self.Message))

        print(" [x] Sent %r" % self.Message)
        self.SendConnection.close()



    def ReceiveQueue(self):
        self.url = 'amqp://' + self.Userid + ":" + self.Userpw + '@jis5376.iptime.org/syncn'
        # self.url = 'amqp://' + "jis" + ":" + "suck0818" + '@jis5376.iptime.org/syncn'
        self.ReceiveConnection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.ReceiveChannel = self.ReceiveConnection.channel()
        # self.ReceiveChannel.queue_declare(queue=self.QueueName)


        self.ReceiveChannel.basic_consume(self.callback, queue=self.QueueName, no_ack=True)

        print(' [*] Wationg for messages. To exit press CTRL+C')
        self.ReceiveChannel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        #example = json.loads(body)['1']['Text']

if __name__ == '__main__':
    Connection = MQ()
    Connection.SendQueue()
    Connection.ReceiveQueue()

