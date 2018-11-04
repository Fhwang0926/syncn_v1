import os


class PathSearch():
    def __init__(self, debug=True):
        self.debug = debug
        # self.path = path

    # Get the files in path
    def listFile(self):
        try:
            self.files = []
            for (dirpath, dirname, filename) in os.walk(self.path):
                self.files = filename
            if self.debug: print("List Files: {0}\n".format(self.files))
            return self.files
        except Exception as e:
            print(e)

    def fileSearch(self, file, extension='', drive="c", detailPath = ''):
        try:
            self.file = file
            self.extension = extension
            self.searchFileList = []
            if detailPath == '':
                self.detailPath = drive + ":/"
            else:
                self.detailPath = detailPath
            if self.extension is '':
                for (path, dirname, files) in os.walk(self.detailPath):
                    for filename in files:
                        self.filename = os.path.splitext(filename)[0]
                        if self.filename == self.file:
                            if self.debug: print("%s\%s" % (path, filename))
                            self.searchFileList.append(path + "\\" + filename)

            else:
                for (path, dirname, files) in os.walk(self.detailPath):
                    for filename in files:
                        self.pullfilename = self.file + "." + self.extension
                        if filename == self.pullfilename:
                            if self.debug: print("%s\%s" % (path, filename))
                            self.searchFileList.append(path + "\\" + filename)
            return self.searchFileList
        except Exception as e:
            print("fileSearch method error, message: {0}\n".format(e))

if __name__ == '__main__':
    test = PathSearch()
    print(test.fileSearch(file="settin3757358g", extension="syncn",detailPath="c:\\python"))