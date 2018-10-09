# auth : wdt0818@naver.com, bluehdh0926@gmail.com
#
import os


class PathSearcher():
    def __init__(self):

        self.setPath(os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + "\AppData\Local\Packages")
        self.is_find = False
        self.findPath = ""
        self.debug = False

    def setPath(self, path):
        self.default_path = path

    def getPath(self):
        return self.default_path

    def getFindPath(self):
        return self.findPath

    def getFindDir(self):
        self.search(self.default_path)
        return self.findDir

    def run(self):
        self.search(self.default_path)
        return self.getFindPath()

    def search(self, path):
        try:
            for _dir in os.listdir(path):
                fullPath = os.path.join(os.path.abspath(path), _dir)
                if os.path.isdir(fullPath) and fullPath.find('MicrosoftStickyNotes_') != -1: self.detailSearch(fullPath)
        except Exception as e:
            print("{0} search, check this {0}".format(__file__, e))
            pass
        if not self.is_find: self.reSearch()

    def detailSearch(self, rootPath):
        for (path, dirname, files) in os.walk(rootPath):
            for f in files:
                fullPath = path + '/' + f
                if fullPath.find("plum.sqlite") != -1:
                    self.findDir = path
                    self.findPath = fullPath
                    self.is_find = True

    def reSearch(self):
        self.is_find = False
        print("can't reSearch")
        pass

    def fileSearch(self, file, extension='', drive="c"):
        self.file = file
        self.extension = extension
        self.searchFileList = []
        if self.extension is '':
            for (path, dirname, files) in os.walk(drive + ":/"):
                for filename in files:
                    self.filename = os.path.splitext(filename)[0]
                    if self.filename == self.file:
                        if self.debug: print("%s\%s" % (path, filename))
                        self.searchFileList.append(path + "\\" + filename)

        else:
            for (path, dirname, files) in os.walk(drive + ":/"):
                for filename in files:
                    self.pullfilename = self.file + "." + self.extension
                    if filename == self.pullfilename:
                        if self.debug: print("%s\%s" % (path, filename))
                        self.searchFileList.append(path + "\\" + filename)
        return self.searchFileList

    def dirSearch(self, dir, drive="c"):
        self.dir = dir.upper()
        self.searchDirList = []
        for (path, dirnames, files) in os.walk(drive + ":/"):
            for dirname in dirnames:
                if dirname.upper() == self.dir:
                    if self.debug: print("%s\%s" % (path, dirname))
                    self.searchDirList.append(path + "\\" + dirname)
        return self.searchDirList

if __name__ == '__main__':
    proc = PathSearcher()
    # proc.dirSearch(dir="syncn")
    # proc.fileSearch(file="setting")
    target = proc.run()
    print(target)