import os, re, pdb, sys, random, string

class DataSet():
    def __init__(self, search, debug=True):
        try:
            # Load module
            self.search = search
            # Use Search angine
            self.path = os.environ['HOME'] + "/.config/xpad"
            self.debug = debug
            self.is_run = False

            # Set xpad files
            self.files = self.search.listFile(dir=self.path)
        except Exception as e:
            print(e)

    # This method pack the data on dictionary format
    def run(self):
        try:
            self.files = self.search.listFile(dir=self.path)
            self.result = {}
            self.is_run = True
            infoFiles = self.getInfo()
            for infoFile in infoFiles:
                data = {}
                infoPath = self.path + "/" + infoFile
                with open(infoPath, "r") as f:
                    contentName = f.readlines()[-1].split()[1]
                    contentPath = self.path + "/" + contentName
                    f.seek(0)
                    with open(contentPath, "r") as ff:
                        data.update({"data": ff.read()})
                    data.update({"info": f.read(),
                                "content": contentName,
                                "infoExtension": self.getExtension(infoPath),
                                "contentExtension": self.getExtension(contentPath)})
                index = infoFile + "/" + contentName
                self.result.update({index: data})
            if self.debug: print("Xpad Data: {0}\n\nNumber of Note: {1}".format(self.result, len(self.result)))
            return self.result
        except Exception as e:
            print(e)

    def getExtension(self, path):
        try:
            tmp = path.split("/")
            extension = tmp[-1].split(".")
            if len(extension) == 2:
                extension = extension[-1]
                return extension
            elif len(extension) == 1:
                extension = "txt"
                return extension
            else:
                if self.debug: print("getextension method error")
        except Exception as e:
            print(e)

    # If you want to show the path, call this method
    def getPath(self):
        return self.path

    # Get only "content-xxxx" files in path
    def getContent(self):
        try:
            # content-xxxxx
            r = re.compile("^[content]+[-]+[a-zA-Z0-9]")
            self.contentFile = list(filter(r.search, self.files))
            if self.debug: print("Content files: {0}\n".format(self.contentFile))
            return self.contentFile
        except Exception as e:
            print(e)

    # Get only "info-xxxx" files in path
    def getInfo(self):
        try:
            # info-xxxxx
            r = re.compile("^[info]+[-]+[a-zA-Z0-9]")
            self.infoFile = list(filter(r.search, self.files))
            if self.debug: print("Info files: {0}\n".format(self.infoFile))
            return self.infoFile
        except Exception as e:
            print(e)


class DataApply():
    def __init__(self, debug=False):
        self.debug = debug
        # self.search = search
        if sys.platform == "linux" or sys.platform == "linux2":
            self.path = os.environ['HOME'] + "/.config/xpad"
        elif sys.platform == "win32":
            self.path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "\AppData\Local\Packages"
        self.data = ''
        self.keyList = []
        self.valueList = []

    # A number of Xpad counter
    def noteNum(self):
        return len(self.data)

    # Distribute key and value
    def dataParse(self, data):
        try:
            # Parameter type check
            if isinstance(data, dict):
                self.data = data
            else:
                print("DataApply Class __init__ error, message: parameter type is not dict, should be input dictionary")

            dist = self.data
            for key,value in dist.items():
                self.keyList.append(key)
                self.valueList.append(dict(value))
            if self.debug:
                print("Key list: {0}\n".format(self.keyList))
                print("Value list: {0}\n".format(self.valueList))
            return True
        except Exception as e:
            print("dataParse method error, message: {0}\n".format(e))

    def dataApply(self):
        try:
            # pdb.set_trace()
            keyList = self.getKeyList()
            valueList = self.getValueList()
            for i in range(self.noteNum()):
                self.dataSet(keyList[i], valueList[i])
                with open(self.path + "/" + self.infoName, "w") as f:
                    f.write(self.infoData)
                    if self.debug: print("made file: {0}".format(self.path + "/" + self.infoName))
                with open(self.path + "/" + self.contentName, "w") as f:
                    f.write(self.contentData)
                    if self.debug: print("made file: {0}".format(self.path + "/" + self.contentName))
        except Exception as e:
            print("dataApply method error, message: {0}\n".format(e))

    def dataSet(self, key, value):
        try:
            self.infoName = key.split("/")[0]
            self.contentName = key.split("/")[1]
            self.infoData = value['info']
            self.contentData = value['data']
            self.infoExtension = value['infoExtension']
            self.contentExtension = value['contentExtension']
            #if self.debug: print("Setting data: {0}{1}{2}{3}{4}{5}\n".format(self.infoName, self.contentName, self.infoData, self.contentData, self.infoExtension, self.contentExtension))
        except Exception as e:
            print("dataSet method error, message: {0}\n".format(e))

    def getKeyList(self):
        return self.keyList

    def getValueList(self):
        return self.valueList


class DataParse():
    def __init__(self, debug=False):
        self.debug = debug

    def run(self, data):
        try:
            self.textList = []
            self.result = {}
            if sys.platform == "linux" or sys.platform == "linux2":
                try:
                    self.msg = data['res']
                    for i in self.msg:
                        self.textList.append(self.msg[i]['Text'])
                    for textList in self.textList:
                        if self.linuxBuild(textList):
                            key = self.info + "/" + self.content
                            source = {"data": self.text,
                                      "content": self.content.split(" ")[1],
                                      "contentExtension": "txt",
                                      "infoExtension": "txt",
                                      "info": self.width + self.height + self.x + self.y + self.follow_font + self.follow_color + self.sticky + self.hidden + self.backrgb + self.textrgb + self.fontname + self.content}
                            self.result.update({key:source})
                    if self.debug: print("Input: Window / Output: Linux ===> Data parsing completed!\n Result: {0}".format(self.result))
                    return self.result
                except KeyError:
                    if self.debug: print("Input: Linux / Output: Linux ===> Data parsing completed!\n Result: {0}".format(self.result))
                    return data
            elif sys.platform == "win32":
                try:
                    self.msg = data['res']
                    self.debug: print("Input: Window / Output: window===> Data parsing completed!\n Result: {0}".format(self.result))
                    return data
                except KeyError:
                    self.msg = data
                    for i in self.msg:
                        self.textList.append(self.msg[i]['data'])
                    cnt = len(self.textList)
                    for textList in self.textList:
                        if self.winBuild(textList):
                            key = str(cnt)
                            source = {"Text":self.Text, "WindowPosition":self.WindowPosition, "Theme":self.Theme}
                            cnt += 1
                            self.result.update({key:source})
                    if self.debug: print("Input: Linux / Output: Window ===> Data parsing completed!\n Result: {0}".format(self.result))
                    return {"res":self.result}


        except Exception as e:
                print("run method error in DataParse class, message: {0}\n".format(e))

        except Exception as e:
            print("run method error in DataParse class, message: {0}\n".format(e))

    def winBuild(self, Text):
        try:
            self.WindowPosition = "V1NERgMAAAABAAAAAff///8AAAAAQAEAAEABAAAAAAA="
            self.Theme = "Yellow"
            self.Text = Text
            return True
        except Exception as e:
            print("Winbuild method error, message: {0}\n".format(e))
            return False

    def linuxBuild(self, text):
        try:
            self.width = "width 300\n"
            self.height = "height 200\n"
            self.x = "x 0\n"
            self.y = "y 0\n"
            self.follow_font = "follow_font 1\n"
            self.follow_color = "follow_color 1\n"
            self.sticky = "sticky 0\n"
            self.hidden = "hidden 0\n"
            self.backrgb = "back rgb (255,238,153)\n"
            self.textrgb = "text rgb (0,0,0)\n"
            self.fontname = "fontname Ubuntu 11\n"
            randomName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.content = "content content-" + randomName + "\n"
            randomName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            self.info = "info-" + randomName
            self.text = text
            return True
        except Exception as e:
            print("linuxBuild method of DataParse class error, message: {0}\n".format(e))
            return False
if __name__ == '__main__':
    test = DataParse()
    print(test.run(data={"info-C9MPRZ/content-ABNPRZ": {"data": "#!@#!@%!@$!$", "content": "content-ABNPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 257\ny 649\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-ABNPRZ\n"}, "info-IMSZRZ/content-0NXZRZ": {"data": "sdfsdfsdf", "content": "content-0NXZRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 105\ny 160\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-0NXZRZ\n"}, "info-86NPRZ/content-VZPPRZ": {"data": "vzxcvzxcvzxcv", "content": "content-VZPPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 182\ny 769\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 0\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-VZPPRZ\n"}, "info-G6MPRZ/content-0ZOPRZ": {"data": "23414234242424", "content": "content-0ZOPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 362\ny 383\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-0ZOPRZ\n"}}))
    # test.run(data={'res': {'4': {'Text': '1. 설치동영상 촬영\n2. MQ 서버 접속 동영상 다시 촬영 \nLOCALHOST로\n3. Search.py 파일검색시 다중 검색 나오면 유저가 선택 할 수 있게 만들기\n4. mq서버에 메세지 전송시 확장자 테그 묶어서 보내기 (json)\n5. 리눅스랑 연동해서 동기화\n6. 해상도 상대적으로 변경해서 스티키노트 위치 설정 버그 고치기\n7.  큐를 가지고 오면 큐 안에 내용 삭제하게하는 법 알아내기\n8. 큐에 최신 데이터 1개만 유지하는 법 알아내기', 'WindowPosition': 'V1NERgMAAAABAAAAAZYCAAAnAAAAdgEAAE8BAAAAIAA=', 'Theme': 'Purple'}, '5': {'Text': '1. email 서버랑 통신하는 auth.py 만들어서 settting.syncn 먼저 얻어야됨\n2. setting.syncn에서 서버 정보 뽑아오는 메소드 MQ.py에 만들기\n3. 데이터 mq에 전송하는 메소드 필요\n4. 데이터 가져와서 적용시키는 메소드 필요\n\n\n외)  xpad설치 경로가 리눅스 다른 버전들도 고정되어 있는지 알아보기', 'WindowPosition': 'V1NERgMAAAABAAAAARAEAABDAAAA5wEAAC8BAAAAAAA=', 'Theme': 'Blue'}, '6': {'Text': '\\id=41e4a17d-8720-4e96-9cb6-b472ed1509fa 1. os = linux -> data = window\n\\id=73391ed2-0550-4ff4-9442-caf08a31867a ->>> content 파일, info파일 랜덤으로 생성후 리눅스 데이터로 파싱하고 리턴\n\\id=f687f5be-ef6c-40ce-adc1-38a8c02f1b15 \n\\id=2394a128-284a-4c26-870f-10f6f77cbd97 2. 0s = window -> data = linux\n\\id=7073d090-03ab-41fd-8aef-2d1c38d94046 ->>> data만 가져오고 나머지는 기본 값으로 파싱후 리턴', 'WindowPosition': 'V1NERgMAAAABAAAAAbACAAARAQAAQAEAAEABAAAAAAA=', 'Theme': 'Charcoal'}}})
