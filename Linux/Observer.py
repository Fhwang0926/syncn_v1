import time, os, threading

class Observer():
    def __init__(self, path, debug=False):
        self.is_run = False
        self.is_send = False
        self.thread_run = False
        self.debug = debug
        self.path = path
        self.send_signal = False
        self.cnt = 0
        self.timestamp = os.path.getmtime(self.path)

    def stop(self):
        self.is_run = False

    def run(self):
        tmp = 0
        try:
            self.is_run = True
            while self.is_run:
                # file changing check
                if self.timestamp != os.path.getmtime(self.path):
                    self.cnt = 0
                    self.timestamp = os.path.getmtime(self.path)
                    # counter start
                    if self.thread_run == False:
                        counter = threading.Thread(target=self.counter)
                        counter.start()

        except Exception as e:
            print("Oberver run method error, message: {0}\n".format(e))

    def counter(self, reset=False):
        self.thread_run = True
        while True:
            time.sleep(1)
            self.cnt += 1
            if self.debug: print("After {0} second, start to sync ".format(5 - self.cnt))
            if self.cnt == 5:
                self.send_signal = True
                self.thread_run = False
                if self.debug: print("Send signal emited\n")
                return
        # if reset:
        #     self.cnt = 0
        # else:
        #     self.cnt += 1

if __name__ == '__main__':
    test = Observer(path="/Users/jeoninsuck/test.rtf", debug=True)
    test.run()
