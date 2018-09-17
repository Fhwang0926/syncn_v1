import pika


class MQ():
    def __init__(self):
        pass
    def SendQueue(self, QueueName, RoutingKey,Message, exchange='',):
        self.SendConnection = pika.BlockingConnection(pika.URLParameters('amqp://jis:suck0818@jis5376.iptime.org'))
        self.SendChannel = self.SendConnection.channel()
        self.SendChannel.queue_declare(queue=QueueName)
        self.SendChannel.basic_publish(exchange=exchange,
                              routing_key=RoutingKey,
                              body=Message)

        print(" [x] Sent %r" % Message)
        self.SendConnection.close()


    def ReceiveQueue(self, QueueName):
        self.ReceiveConnection = pika.BlockingConnection(pika.URLParameters('amqp://jis:suck0818@jis5376.iptime.org'))
        self.ReceiveChannel = self.ReceiveConnection.channel()
        self.ReceiveChannel.queue_declare(queue=QueueName)

        self.ReceiveChannel.basic_consume(self.callback,
                              queue=QueueName,
                              )
        print(' [*] Wationg for messages. To exit press CTRL+C')
        self.ReceiveChannel.start_consuming()

    def callback(self,ch, method, properties, body):
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
    Connection = MQ()
    Connection.SendQueue("hello","hello","What the fuck!")
    Connection.ReceiveQueue("hello")
