import os
import re
import pdb

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
                    #data.update({"info": f.read()})
                    #data.update({"contentemt": contentName})
                    #data.update({"infoPath": self.getExtension(infoPath)})
                    #data.update({"contentPath": self.getExtension(contentPath)})
                    data.update({"info": f.read(),
                                "content": contentName,
                                "infoExtension": self.getExtension(infoPath),
                                "contentExtension": self.getExtension(contentPath)})
                index = infoFile + "/" + contentName
                self.result.update({index: data})
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
    print()
    print("Number of note: ", len(ob.run()))

