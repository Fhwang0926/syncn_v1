import pika


class MQ():
    def __init__(self):
        try:
            self.para = None
            self.con = None
            self.ch = None
            self.userId = None
            self.userPwd = None
            self.url = None
        except Exception as e:
            print(e)


    def connection(self):
        self.para = pika.URLParameters("amqp://{0}:{1}@{2}:{3}/{4}".format(self.userId, self.userPwd, self.url, self.port, self.vhost))
        self.con = pika.BlockingConnection(self.para)
        self.ch = self.con.channel()
