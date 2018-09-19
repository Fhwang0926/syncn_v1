#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com

import sqlite3
import PathSearch
import pydash as _
import uuid
import json
import time
#windows RS4 under version location is C: \Users\Username\AppData\Roaming\Microsoft\Sticky Notes\StickyNotes.snt


class DAO():
    def __init__(self, fullpath):
        # set variables
        self.fullpath = fullpath if fullpath else PathSearch.SetPath().result
        self.path = ''
        self.db = None
        self.conn = None
        self.id = None;
        self.noteCnt = 0;
        self.temp = None;
        self.debug = True;
        
        # set function
        self.init(self.fullpath)
        self.readUser()
        self.dumpBackupOneRow()
        pass

    def read(self):
        # self.readUser()
        col = ["Text", "WindowPosition", "Theme"]
        rs = self.db.execute("SELECT {0} FROM Note WHERE ParentId='{1}' limit 1".format(_.join(col, ','), self.id))
        return self.convert(rs)
    
    def readUser(self): # version 1.0 consider 1 account in host
        col = "id"
        rs = self.db.execute("SELECT " + col + " FROM User limit 1")
        def parser(r): self.id = r[0]
        _.for_each(rs, parser)
        

    def init(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.db = self.conn.cursor()
        pass

    def update(self, notes):
        try:
            pass
        except Exception as e:
            eprint(e)
            pass
        if not notes: return print("given 1 args(type=dict)")
        if not (type(notes) is dict): return print("args must be a dict")

        # question to user before processing sync 
        # self.db.execute('TRUNCATE Note') # clean
        # insert format { Text, WindowPosition, Id, ParentId, Theme, CreatedAt, UpdatedAt }
        # self.readUser()
        self.temp = notes;
        def parser(k):
            cols = ["Text", "WindowPosition", "Id", "ParentId", "Theme", "CreatedAt", "UpdatedAt"]
            parms = [self.temp[k]['Text'], self.temp[k]['WindowPosition'], uuid.uuid1(), self.id, self.temp[k]['Theme'], int(time.time()), int(time.time())]
            # for index in range(0, len(parms)):
            #     parms[index] = "'{0}'".format(parms)
            #     pass
            if self.debug:
                for index in range(0, len(cols)):
                    print(cols[index], " = ", parms[index])
                pass
            
            sql = "INSERT INTO Note ({0}) VALUES ('{1}')".format(_.join(cols, ','), _.join(parms, "','"))
            self.db
            print(sql)
            self.db.execute(sql)
            # notes.update({ str(self.noteCnt) : { "Text" : r[0], "WindowPosition" : r[1], "Theme" : r[2] } })

        _.for_each(_.keys(notes), parser)
        self.temp = None;
    
    def dumpBackupOneRow(self):
        col = ["*"]
        rs = self.db.execute("SELECT {0} FROM Note WHERE ParentId='{1}' limit 1".format(_.join(col, ','), self.id))
        self.backup = self.convert(rs)

    def convert(self, items):
        notes = {}
        def parser(r):
            self.noteCnt+=1
            notes.update({ str(self.noteCnt) : { "Text" : r[0], "WindowPosition" : r[1], "Theme" : r[2] } })

        _.for_each(items, parser)
        return notes

    def check(self):
        return self.read(chk=True)

# SELECT * FROM note

if __name__ == '__main__':
    # No remove this comment
    # C:\Users\hdh09\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite
    dao = DAO("C:\\Users\\hdh09\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite")
    # print(dao.read())
    # if update input type is string, using json parser
    data = '{"1": {"Text": "test", "WindowPosition": "V1NERgMAAAABAAAAAaoJAADcAQAAEgIAANcCAAAAAAA=", "Theme": "Yellow"}}'
    dao.update(json.loads(data))
    # dao.update("132")

    pass
