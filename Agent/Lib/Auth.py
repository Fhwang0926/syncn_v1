
import requests
import time
import json


class EmailCert():
    def __init__(self):
        self.debug = True
        self.url = ''
        self.email = ''
        self.otpCode = ''
        self.sub = {
            "code" : "/code/",
            "account" : "/account/",
            "remove" : "/remove/",
        }

    def build(self, url, email):
        self.url = url if url.find("://") else "http://"+url
        self.email = email
        self.otpCode = ''
    
    def requestAuthClear(self):
        self.otpCode = ''
        print("OTP Code Clear, try createOTP")
    
    def buildClear(self):
        self.otpCode = ''
        self.email = ''
        self.url = ''
        print("Reset build, try createOTP")
    
    def createOTP(self):
        try:
            otpResult = requests.post(url=self.url + self.sub['code'], data=self.email)
            if otpResult.status_code == 200:
                self.otpCode = otpResult.json()['res']
                if self.debug:
                    print(otpResult.status_code, " : ", otpResult.json()['e'])
            else:
                print(otpResult.status_code, " : ", "Server Connection failed, Check your network!")
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
        except Exception as e:
            print(e)

    def authOTP(self):
        try:
            authResult = requests.get(url=self.url + self.sub['account'] + self.otpCode)
            if authResult.status_code == 200:
                setting = open("Setting.syncn", 'w')
                setting.write(json.dump(authResult.json()['res']))
                setting.close()
                print("save setting!! ready to sync")
                if self.debug: print(authResult.text)
            else:
                print("authResult.status_code, Check your Email and verify auth URL Link")
                if self.debug: print(authResult.json()['e'])
        except Exception as e:
            print(e)
            pass
        

if __name__ == '__main__':

    client = EmailCert()
    client.build("http://syncn.club:9759","hdh0926@naver.com")
    client.createOTP()
    time.sleep(60)
    client.authOTP()
