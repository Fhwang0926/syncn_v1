import os
import re

class DataSet():
    def __init__(self, debug=False):
        try:
            # Use Search angine
            self.path = os.environ['HOME'] + "/.config/xpad"
            self.debug = debug
            self.is_run = False

            # Set xpad files
            self.listFile()
        except Exception as e:
            print(e)

    # This method pack the data on dictionary format
    def run(self):
        try:
            self.result = {}
            self.is_run = True
            infoFiles = self.listFile()
            for infoFile in infoFiles:
                data = {}
                with open(self.path + "/" + infoFile, "r") as f:
                    contentName = f.readlines()[-1].split()[1]
                    f.seek(0)
                    with open(self.path + "/" + contentName) as ff:
                        data.update({"data": ff.read()})
                    data.update({"info": f.read()})
                    data.update({"content": contentName})
                index = infoFile + "/" + contentName
                self.result.update({index: data})
            return self.result
        except Exception as e:
            print(e)

    def getExtension(self):


    # If you want to show the path, call this method
    def getPath(self):
        return self.path

    # Get the files in path
    def listFile(self):
        try:
            self.files = []
            for (dirpath, dirname, filename) in os.walk(self.path):
                self.files = filename
            if self.debug: print(self.files)
            return self.files
        except Exception as e:
            print(e)
    # Get only "content-xxxx" files in path
    def getContent(self):
        try:
            # content-xxxxx
            r = re.compile("^[content]+[-]+[a-zA-Z0-9]")
            self.contentFile = list(filter(r.search, self.files))
            if self.debug: print(self.contentFile)
            return self.contentFile
        except Exception as e:
            print(e)

    # Get only "info-xxxx" files in path
    def getInfo(self):
        try:
            # info-xxxxx
            r = re.compile("^[info]+[-]+[a-zA-Z0-9]")
            self.infoFile = list(filter(r.search, self.files))
            if self.debug: print(self.infoFile)
            return self.infoFile
        except Exception as e:
            print(e)


if __name__ == '__main__':
    ob = DataSet()
    print(ob.run())

