import pika
import Search, Setting

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
            # self.vhost = 'syncn'
            # self.port = '5672'
            # self.userId = 'syncn'
            # self.userPwd = 'syncn'
            # self.url = 'jis5376.iptime.org'
            # self.queue = "djfjsjeifjsj"

        except Exception as e:
            print(e)

    def build(self, data):
        try:
            self.config = data
            self.queue = self.config['q']
            self.userId = self.config['id']
            self.userPwd = self.config['pw']
            self.url = self.config['host']
            self.port = self.config['port']
            self.vhost = self.config['vhost']
            # self.init = self.config['init']
        except Exception as e:
            print("build method error, message: {0}".format(e))

    # def run(self, msg):
    #     try:
    #         self.connection()
    #         self.sendMsg(exchange="msg", routing_key=self.queue, msg=msg)
    #     except Exception as e:
    #         print("MQ run method error, message: {0}".format(e))


    def connection(self):
        try:
            self.para = pika.URLParameters("amqp://{0}:{1}@{2}:{3}/{4}".format(self.userId,
                                                                               self.userPwd,
                                                                               self.url,
                                                                               self.port,
                                                                               self.vhost))
            self.con = pika.BlockingConnection(self.para)
            if self.debug: print("Connected with Server\n")
        except Exception as e:
            print("connection method error, message: {0}".format(e))

    def disconnection(self):
        return self.con.close()

    def createChannel(self):
            return self.con.channel()

    def makeQueue(self, queue, passive=False, durable=True, exclusive=False, auto_delete=False, arguments=None):
        ch = self.createChannel()
        ch.queue_declare(queue=queue, passive=passive, durable=durable, exclusive=exclusive,
                              auto_delete=auto_delete, arguments=arguments)
        if self.debug: print("Making Queue is Completed\n")

    def makeExchange(self, exchange, exchange_type='direct', passive=False, durable=True, auto_delete=False, internal=False, arguments=None):
        ch = self.createChannel()
        ch.exchange_declare(exchange=exchange, exchange_type=exchange_type, passive=passive, durable=durable,
                                 auto_delete=auto_delete, internal=internal, arguments=arguments)
        if self.debug: print("Making Exchange is Completed\n")

    def queueBind(self, exchange, queue):
        ch = self.createChannel()
        ch.queue_bind(exchange=exchange, queue=queue)
        if self.debug: print("Binding is completed\nExchange: {0} ====> Queue: {1}\n".format(exchange, queue))

    def sendMsg(self, exchange='', routing_key='', msg='', properties=None, mandatory=False, immediate=False):
        try:
            ch = self.createChannel()
            ch.basic_publish(exchange=exchange, routing_key=routing_key, body=msg, properties=None, mandatory=False, immediate=False)
            if self.debug: print("Send Message: {0}\nrouting_key: {1}\nexchange: {2}\n".format(msg, routing_key, exchange))
            return True
        except Exception as e:
            print("sendMsg method error, message: {0}".format(e))

    def receiveMsg(self, queue, ack=False):
        try:
            ch = self.createChannel()
            self.method_frame, self.header_frame, self.body = ch.basic_get(queue=queue)
            if self.method_frame.message_count == 0:
                if self.debug:
                    print("Number of Message: {0}, The delivery_tag was not sent\n".format(self.method_frame.message_count))
                    print("Receive Message: {0}\n".format(self.body))
                return self.body
            elif self.method_frame.message_count > 0:
                if ack == True:
                    ch.basic_ack(self.method_frame.delivery_tag)
                if self.debug: print("Number of Message: {0}, The delivery_tag was sent\n".format(self.method_frame.message_count))
                return self.body
            else:
                if self.debug: print("Number of Message: {0}, No Message in the queue\n".format(self.method_frame.message_count))
                return self.body
        except Exception as e:
            print("receiveMsg method error, message: {0}".format(e))



if __name__ == '__main__':
    test = MQ()
    # test.connection()
    test.sendMsg(routing_key="test", msg=" It's a test MSG")
    # test.sendMsg(routing_key="test", msg="Please get the MSG")
    # test.receiveMsg(queue="test")
