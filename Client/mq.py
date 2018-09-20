import pika
import json
# import NoteSql

class MQ():
    def __init__(self):
        self.build()
        self.connection = pika.BlockingConnection(pika.URLParameters(self.Url))
        self.channel = self.connection.channel()
        if(self.channel): print(self.Url+' connected')
        
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
        
    
    def makeQueue(self, name='', durable=True, opt={}):
        self.channel.queue_declare(name, durable, opt)
        pass
    
    def makeExchange(self, name='', ex_type='', opt={}):
        self.channel.exchange_declare(name, ex_type, opt)
        pass

    def makeBind(self, exchange='', queue='', routing_key=''):
        self.channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)
        pass

    def makeUser(self):
        # to be make when use it
        pass

    def removeQueue(self):
        # to be make when use it
        pass

    def removeExchange(self):
        # to be make when use it
        pass

    def removeBind(self, exchange='', queue=''):
        self.channel.queue_unbind(exchange=exchange, queue=queue)
        pass

    def removeUser(self):
        # to be make when use it
        pass
    
    
    def getChannel(self):
        return self.channel
    
    def createChannel(self):
        return self.connection.channel()

    def publishExchange(self, exchange='', routing_key='', msg='', opt={}):
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=msg)
        print(" [x] publishExchange %r" % msg)
    
    def publishQueue(self, queue='', msg='', opt={}):
        self.channel.basic_publish(routing_key=queue, exchange='', body=msg)
        print(" [x] publishQueue %r" % msg)

    def worker(self, func=None, queue=''):
        print(' [*] start working')
        func = func if func else self.callback
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(func, queue=queue, no_ack=False)
        self.channel.start_consuming()

    def callback(serlf, ch, method, properties, msg):
            print(" [x] Received %r" % msg)
            ch.basic_ack(delivery_tag = method.delivery_tag)


if __name__ == '__main__':
    mq = MQ()

    mq.makeQueue('test')
    mq.makeExchange(name='test', ex_type='fanout')
    mq.makeBind(exchange='test', queue='test')

    mq.publishExchange(exchange='test', msg='test')
    mq.publishQueue(queue='test', msg='test')

    mq.worker(queue='test')

