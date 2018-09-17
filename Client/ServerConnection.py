import pika
import json

class MQ():
    def __init__(self):
        with open("Setting.syncn", 'r') as configfile:
            self.ServerData = json.load(configfile)
        self.QueueName = self.ServerData['q']
        self.Userid = self.ServerData['id']
        self.Userpw = self.ServerData['pw']
        self.RoutingKey = ''
        self.Message = ""
        self.exchange = ""

    def SendQueue(self):
        self.SendConnection = pika.BlockingConnection(pika.URLParameters('amqp://' ,
                                                                         + self.Userid ,
                                                                         + ":",
                                                                         + self.Userpw,
                                                                         + '@jis5376.iptime.org'))
        self.SendChannel = self.SendConnection.channel()
        self.SendChannel.queue_declare(queue=self.QueueName)
        self.SendChannel.basic_publish(exchange=self.exchange,
                              routing_key=self.RoutingKey,
                              body=self.Message)

        print(" [x] Sent %r" % self.Message)
        self.SendConnection.close()



    def ReceiveQueue(self):
        self.ReceiveConnection = pika.BlockingConnection(pika.URLParameters('amqp://' ,
                                                                         + self.Userid ,
                                                                         + ":",
                                                                         + self.Userpw,
                                                                         + '@jis5376.iptime.org'))
        self.ReceiveChannel = self.ReceiveConnection.channel()
        self.ReceiveChannel.queue_declare(queue=self.QueueName)

        self.ReceiveChannel.basic_consume(self.callback,
                              queue=self.QueueName,
                              )
        print(' [*] Wationg for messages. To exit press CTRL+C')
        self.ReceiveChannel.start_consuming()

    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
<<<<<<< HEAD
    Connection = MqConnection()
=======
    Connection = MQ()
    Connection.SendQueue("hello","hello","What the fuck!")
    Connection.ReceiveQueue("hello")
>>>>>>> 85184b737569c272e270f7c96addb2bfeea366ed
