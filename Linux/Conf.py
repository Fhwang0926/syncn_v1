import json, os, sys
# import Search

class Conf():
    def __init__(self, search, debug=True):
        self.debug = debug
        self.path = os.path.dirname(os.path.dirname(__file__))
        # init
        self.search = search

    def read(self):
        try:
            self.file = self.search.fileSearch(file="setting", extension="syncn", detailPath=self.path)[0]
            if self.debug: print("setting file path: {0}\n".format(self.path))
            with open(self.file, 'r') as f:
                self.data = json.loads(f.read())
                if self.debug: print("Setting file data: {0}\n".format(self.data))
            return self.data
        except Exception as e:
            print("read method error, message: {0}\n".format(e))
            return False

    def write(self, source):
        try:
            # if one file
            # self.path = os.getcwd()
            if sys.platform == "win32":
                with open(self.path + "\\setting.syncn", 'w') as f:
                    source = json.dumps(source)
                    f.write(source)
            elif sys.platform == "linux" or sys.platform == "linux2":
                with open(self.path + "/setting.syncn", 'w') as f:
                    source = json.dumps(source)
                    f.write(source)
        except Exception as e:
            print("write method error, message: {0}\n".format(e))

if __name__ == '__main__':
    # test = Conf(search=Search.PathSearch())
    # test.read()
    test = Conf(search='')
