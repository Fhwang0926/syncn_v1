
import requests
import time
import json


class EmailCert():
    def __init__(self, Url, EmailAddress):
        self.url = Url
        self.EmailAddress = EmailAddress

    # Log in Authentication URL Request
    def SendMyInfo(self):
        try:
            self.Post = requests.post(url=self.url, data=self.EmailAddress)
        except requests.exceptions.ConnectionError:
            print("requests.exceptions.ConnectionError")
            return
        except:
            raise
            return

        if self.Post.status_code == 200:
            self.ResponseBody = self.Post.json()['res']
            # print(self.Post.status_code)
            # self.ResponseBody = self.ResponseBody.split(".")
            print(self.Post.json()['res'])

        else:
            print(self.Post.status_code)
            print("Check your network!")
            return

        # time.sleep(3)
        self.ReceiveCheckCode()

    # Authentication URL confirm message
    def ReceiveCheckCode(self):
        self.ReceiveConfirmMessage= requests.get(url=self.url + "/account/" + self.ResponseBody)
        print(self.ReceiveConfirmMessage.url)
        if self.ReceiveConfirmMessage.status_code == 200:
            self.ConfigData = (self.ReceiveConfirmMessage.json()['res'])

            with open("Setting.syncn", 'w') as settingfile:
                json.dump(self.ConfigData, settingfile)
            print(self.ReceiveConfirmMessage.text)
        else:
            print(self.ReceiveConfirmMessage.status_code)
            print(self.ReceiveConfirmMessage.text)
            print("Check your Email and Certify by URL Link")

if __name__ == '__main__':

    test = EmailCert("http://syncn.club:9759","wdt0818@naver.com")
    test.SendMyInfo()
