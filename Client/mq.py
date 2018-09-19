import pika
import json
# import NoteSql

class MQ():
    def __init__(self):
        self.build()
        self.connection = pika.BlockingConnection(pika.URLParameters(self.Url))
        self.channel = self.connection.channel()
        
    def build(self):
        self.ServerData = json.load(open("Setting.syncn", 'r'))
        self.QueueName = self.ServerData['q']
        self.Userid = self.ServerData['id']
        self.Userpw = self.ServerData['pw']
        self.Domain = "jis5376.iptime.org"
        # self.Domain = self.ServerData['domain'] if self.ServerData['domain'] else "jis5376.iptime.org" # this info make config or get domain later
        # self.Port = self.ServerData['port'] if self.ServerData['port'] else 5672 # this info make config or get domain later
        self.port = 5672
        self.Url = 'amqp://' + self.Userid + ":" + self.Userpw + '@'+self.Domain+'/syncn'
        self.RoutingKey = self.QueueName
        self.exchange = "msg"
        self.Message = "test"
    
    def makeQueue(self, name, opt):
        self.channel.queue_declare(name, opt)
        pass
    
    def makeExahnge(self, name, ex_type, opt):
        self.channel.exchange_declare(exchange=name, exchange_type=ex_type, options=opt)
        pass

    def makeBind(self, exchange, queue):
        self.channel.queue_bind(exchange=exchange, queue=queue)
        pass

    def makeUser(self):
        pass

    def makeQueue(self):
        pass
    def removeExchange(self):
        pass
    def removeBind(self, exchange, queue):
        self.channel.queue_bind(exchange=exchange, queue=queue)
        pass
    def removeUser(self):
        pass
    
    
    def getChannel(self):
        return self.channel
    
    def createChannel(self):
        return self.connection.channel()

    def publishExchange(self, queue, exchange, routing_key, msg, opt):
        self.Channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, options=opt)
        print(" [x] publishExchange %r" % msg)
    
    def publishQueue(self, queue, type, msg, opt):
        self.Channel.basic_publish(queue=queue, routing_key=routing_key, body=msg, options=opt)
        print(" [x] publishQueue %r" % msg)

    def ReceiveQueue(self, func, queue, opt):
        print(' [*] start working')
        cb = func if func else self.callback
        self.channel.basic_consume(cb, queue=self.QueueName, no_ack=False, options=opt)

    def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)


if __name__ == '__main__':
    mq = MQ()
    try:
        mq.makeQueue('test')
    except exception as e:
        pass

    mq.publishQueue(queue='test', msg='test')
    mq.working(queue='test')

