import requests, re

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

    def emailCheck(self, email):
        r = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z0-9+-_.]")
        if r.match(email) == None:
            return False
        else:
            if self.debug: print(r.match(email))
            return True

    def sendUrl(self):
        if self.emailCheck(self.email):
            postUrl = requests.post(url=self.server + self.sub['code'], data=self.email)
            if self.debug: print("")
            if postUrl.status_code == 200:
                code = postUrl.json()['res']




if __name__ == '__main__':
    test = EmailCert(debug=True)
    test.emailCheck(email="wdt0818@naver.com")