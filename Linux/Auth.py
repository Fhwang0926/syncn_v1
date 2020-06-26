import requests, re
import time

class EmailCert():
    def __init__(self, debug=False):
        self.debug = debug
        self.server = ''
        self.email = ''
        self.sub = {
            "code": "/code/",
            "account": "/account/",
            "remove": "/remove/",
        }
    def build(self, email):
        try:
            if self.emailCheck(email):
                self.email = email
                self.server = "http://jis5376.iptime.org:9759"
                return True
            else:
                return False
        except Exception as e:
            print("build method error, message: {0}".format(e))

    # Inputed email confirm
    def emailCheck(self, email):
        r = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z0-9+-_.]")
        if r.match(email) == None:
            return False
        else:
            if self.debug: print(r.match(email))
            return True

    # Send the Url to email to confirm the user
    def sendUrl(self):
        try:
            postUrl = requests.post(url=self.server + self.sub['code'], data=self.email)
            if postUrl.status_code == 200:
                self.code = postUrl.json()['res']
                if self.debug: print("State code: {0}, message: {1}".format(postUrl.status_code, self.code))
                return True
            else:
                print("Status code: {0}, Can not post to server, restart\n".format(postUrl.status_code))
        except Exception as e:
            print("sendUrl method error, message: {0}".format(e))
        return False

    # After click the Url, request the info of the MQ server to email server
    def getServerInfo(self):
        try:
            infoRequest = requests.get(url=self.server + self.sub['account'] + self.code)
            if infoRequest.status_code == 200:
                rs = infoRequest.json()
                if self.debug: print("Status code: {0}, Message: {1}\n".format(infoRequest.status_code, rs))
                return rs
            else:
                print("Status code: {0}, please check your email".format(infoRequest.status_code))
        except Exception as e:
            print("getServerInfo mehtod error, message: {0}".format(e))

if __name__ == '__main__':
    test = EmailCert(debug=True)
    test.build(email="wdt0818@naver.com")
    test.sendUrl()
    time.sleep(10)
    test.getServerInfo()