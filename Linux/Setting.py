import os, re, pdb

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
        self.path = os.environ['HOME'] + "/.config/xpad"
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
            if self.debug: print("Setting data: {0}{1}{2}{3}{4}{5}\n".format(self.infoName, self.contentName, self.infoData, self.contentData, self.infoExtension, self.contentExtension))
        except Exception as e:
            print("dataSet method error, message: {0}\n".format(e))

    def getKeyList(self):
        return self.keyList

    def getValueList(self):
        return self.valueList

if __name__ == '__main__':
    test = DataApply(data={"info-C9MPRZ/content-ABNPRZ": {"data": "#!@#!@%!@$!$", "content": "content-ABNPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 257\ny 649\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-ABNPRZ\n"}, "info-IMSZRZ/content-0NXZRZ": {"data": "sdfsdfsdf", "content": "content-0NXZRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 105\ny 160\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-0NXZRZ\n"}, "info-86NPRZ/content-VZPPRZ": {"data": "vzxcvzxcvzxcv", "content": "content-VZPPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 182\ny 769\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 0\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-VZPPRZ\n"}, "info-G6MPRZ/content-0ZOPRZ": {"data": "23414234242424", "content": "content-0ZOPRZ", "contentExtension": "txt", "infoExtension": "txt", "info": "width 308\nheight 200\nx 362\ny 383\nfollow_font 1\nfollow_color 1\nsticky 0\nhidden 1\nback rgb(255,238,153)\ntext rgb(0,0,0)\nfontname Ubuntu 11\ncontent content-0ZOPRZ\n"}}
)
    test.dataParse()
    test.dataApply()
