import time, os

class Observer():
    def __init(self, path, debug=False):
        self.is_run = False
        self.debug = debug
        self.path = path
        self.cnt = 0
        self.timestamp = os.path.getmtime(self.path)

    def run(self):
        try:
            self.is_run = True
            while self.is_run:
                time.sleep(1)
                if self.timestamp != os.path.getmtime(self.path):
                    self.counter()
                    if self.timestamp == 5:
                        
                else:
                    continue
        except Exception as e:
            print("Oberver run method error, message: {0}".format(e))

    def counter(self, reset=False):
        if reset:
            self.cnt = 0
        else:
            self.cnt += 1