import pika


class MQ():
    def __init__(self, debug=True):
        try:
            self.debug = debug
            self.para = None
            self.con = None
            self.ch = None
            self.vhost = "syncn"
            self.port = 5672
            self.userId = "syncn"
            self.userPwd = "syncn"
            self.url = "jis5376.iptime.org"

            # set connection
            # self.connection()
        except Exception as e:
            print(e)

    def run(self):
        try:
            self.connection()
            # self.makeQueue(queue="test")
            self.queueBind(exchange="msg", queue="test")
            self.sendMsg(msg="It's a test msg",routing_key="test")
        except Exception as e:
            print(e)
        finally:
            self.con.close()

    def connection(self):
        self.para = pika.URLParameters("amqp://{0}:{1}@{2}:{3}/{4}".format(self.userId,
                                                                           self.userPwd,
                                                                           self.url,
                                                                           self.port,
                                                                           self.vhost))
        self.con = pika.BlockingConnection(self.para)
        self.ch =  self.con.channel()
        if self.debug: print("Connected with Server\n")

    def makeQueue(self, queue, passive=False, durable=True, exclusive=False, auto_delete=False, arguments=None):
        self.ch.queue_declare(queue=queue, passive=passive, durable=durable, exclusive=exclusive,
                              auto_delete=auto_delete, arguments=arguments)
        if self.debug: print("Making Queue is Completed\n")

    def makeExchange(self, exchange, exchange_type='direct', passive=False, durable=True, auto_delete=False, internal=False, arguments=None):
        self.ch.exchange_declare(exchange=exchange, exchange_type=exchange_type, passive=passive, durable=durable,
                                 auto_delete=auto_delete, internal=internal, arguments=arguments)
        if self.debug: print("Making Exchange is Completed\n")

    def queueBind(self, exchange, queue):
        self.ch.queue_bind(exchange=exchange, queue=queue)
        if self.debug: print("Binding is completed\nExchange: {0} ====> Queue: {1}\n".format(exchange, queue))


    def sendMsg(self, exchange='', routing_key='', msg='', properties=None, mandatory=False, immediate=False):
        self.ch.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=None, mandatory=False, immediate=False)
        if self.debug: print("Send Message: {0}\nrouting_key: {1}\nexchange: {2}\n".format(msg, routing_key, exchange))

    def receiveMsg(self,):

if __name__ == '__main__':
    test = MQ()
    test.run()