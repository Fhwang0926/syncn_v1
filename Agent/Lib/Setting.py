#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com, suck0818@gmail.com
# setting management json

import json

class syncn(object):
    def __init__(self, path):
        try:
            self.path = path
            self.config = json.loads(open(path, 'r').read())
        except Exception as e:
            print(e)
            pass
        
    def readSetting(self):
        return json.loads(open(self.path, 'r').read())
    
    def writeSetting(self, data):
        setting = open(self.path, 'w')
        data = json.dumps(data) if isinstance(data, dict) else data
        setting.write(data)
        return setting.close()
        
    def addSetting(self, key, value):
        rs = self.readSetting()
        rs[str(key)] = value
        return self.writeSetting(rs)
        
if __name__ == '__main__':
    import time
    test = Setting('../setting.syncn')
    test.addSetting("tmp", "asd")
    print(test.config)