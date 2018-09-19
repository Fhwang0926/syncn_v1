import os

class SetPath():
    def __init__(self):
        self.full_path = "C:\\Users\\" + os.getlogin() + "\\AppData"
        self.search()

    def search(self):
        # try:
        #     filenames = os.listdir(self.full_path)
        #     for filename in filenames:
        #         full_filename = os.path.join(self.full_path, filename)
        #         if os.path.isdir(full_filename):
        #             self.search(full_filename)
        #         else:
        #             if filename == 'plum.sqlite':
        #                 return full_filename
        # except PermissionError:
        #     pass
        for (path, dir, files) in os.walk(self.full_path):
            for filename in files:
                if filename == "plum.sqlite":
                    self.result = path + "\\" + filename
                    return self.result


if __name__ == '__main__':
    pass