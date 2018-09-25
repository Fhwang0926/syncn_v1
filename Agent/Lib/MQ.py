#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com

import pika, json, os, sys

class MQ():
    def __init__(self, debug=False):
        try:
            self.debug = debug
            self.build()
            self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
            self.channel = self.connection.channel()
            if(self.channel): print('PROTOCOL : '+self.url+' connected')
        except Exception as e:
            print(e)
            pass
        
    def build(self):
        try:
            self.config = json.loads(open("../Setting.syncn", 'r').read())
            self.queue = self.config["q"]
            self.id = self.config["id"]
            self.pw = self.config["pw"]
            self.host = self.config["host"]
            self.port = self.config["port"]
            self.vhost = self.config["vhost"]
            self.url = "amqp://{0}:{1}@{2}:{3}/{4}".format(self.id, self.pw, self.host, self.port, self.vhost)
            self.rKey = self.queue
            self.ex_msg = "msg"
            self.ex_cmd = "cmd"
        except Exception as e:
            print(e)
            pass
        
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
        # to be make when use it
        # self.channel.queue_unbind(exchange=exchange, queue=queue)
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
    try:
        mq = MQ()
        # mq.makeQueue('test')
        # mq.makeExchange(name='test', ex_type='fanout')
        # mq.makeBind(exchange='test', queue='test')
        # mq.publishExchange(exchange='test', msg='test')
        # mq.publishQueue(queue='test', msg='test')
        mq.worker(queue='c.73ff7d371f80571ed86a77726ad25330')
    except Exception as e:
        print("Error, check this {0}".format(e))
        pass
    

