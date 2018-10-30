import pika
import Setting, Conf

class MQ():
    def __init__(self, debug=False):
        try:
            # get data
            # self.Msg = Setting.DataSet()

            self.debug = debug
            self.para = None
            self.con = None
            self.ch = None
            self.vhost = ''
            self.port = ''
            self.userId = ''
            self.userPwd = ''
            self.url = ''

            # init
            self.build()
            self.connection()
        except Exception as e:
            print(e)

    def build(self):
        self.config = Conf.Conf().read()
        self.queue = self.config['q']
        self.userId = self.config['id']
        self.userPwd = self.config['pw']
        self.url = self.config['host']
        self.port = self.config['port']
        self.vhost = self.config['vhost']
        self.init = self.config['init']


    # def run(self):
    #     try:
    #         self.connection()
    #         # self.makeQueue(queue="test")
    #         self.queueBind(exchange="msg", queue="test")
    #         self.sendMsg(msg="It's a test msg",routing_key="test")
    #     except Exception as e:
    #         print(e)
    #     finally:
    #         self.con.close()

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
        try:
            self.ch.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=None, mandatory=False, immediate=False)
            if self.debug: print("Send Message: {0}\nrouting_key: {1}\nexchange: {2}\n".format(msg, routing_key, exchange))
        except Exception as e:
            print("sendMsg method error, message: {0}".format(e))

    def receiveMsg(self, queue):
        try:
            method_frame, header_frame, body = self.ch.basic_get(queue=queue)
            if method_frame.message_count == 0:
                if self.debug:
                    print("Number of Message: {0}, The delivery_tag was not sent\n".format(method_frame.message_count))
                    print("Receive Message: {0}\n".format(body))
            elif method_frame.message_count > 0:
                self.ch.basic_ack(method_frame.delivery_tag)
                if self.debug: print("Number of Message: {0}, The delivery_tag was sent\n".format(method_frame.message_count))
            else:
                if self.debug: print("Number of Message: {0}, No Message in the queue\n".format(method_frame.message_count))
        except Exception as e:
            print("receiveMsg method error, message: {0}".format(e))


if __name__ == '__main__':
    test = MQ()
    test.sendMsg(routing_key=test.queue, msg=Setting.DataSet())
    # test.sendMsg(routing_key="test", msg="Please get the MSG")
    # test.receiveMsg(queue="test")