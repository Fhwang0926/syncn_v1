#!/usr/bin/python
# -*- coding: utf8 -*-
# auth : bluehdh0926@gmail.com, suck0818@gmail.com

import sqlite3, uuid, json, time
import pydash as _


class DAO():
    def __init__(self, fullpath='', debug=False):
        # set variables
        self.fullpath = fullpath
        # if fullpath else Search.PathSearcher().run(file="plum", detailPath=Search.PathSearcher().getPath())[0]
        self.path = ''
        self.db = None
        self.conn = None
        self.id = None
        self.noteCnt = 0
        self.temp = None
        self.debug = debug
        self.is_dbFile = True
        self.is_textFile = False

        # file type check
        # self.fileCheck(self.fullpath)
        if self.is_dbFile:
            # set function
            self.initDb(self.fullpath)
            self.readUser()
            self.dumpBackupOneRow()

        elif self.is_textFile:
            self.initText(self.fullpath)

        # set function
        # self.init(self.fullpath)
        # self.readUser()
        # self.dumpBackupOneRow()

    def fileCheck(self, file):
        self.file = file.split("\\")
        self.extension = self.file[-1].split(".")[-1]
        try:
            if "sql" in self.extension:
                self.is_dbFile = True
            else:
                self.is_textFile = True
        # other file check
        except Exception as e:
            if self.debug: print(e)

    def close(self):
        try:
            return { "res" : sle.conn.close() }
        except Exception as e:
            return { "e" : e }

    def read(self):

        if self.is_dbFile:
            try:
                # self.readUser()
                col = ["Text", "WindowPosition", "Theme"]
                limit = "limit 2" if self.debug else ''
                rs = self.db.execute("SELECT {0} FROM Note WHERE ParentId='{1}' {2}".format(_.join(col, ','), self.id, limit))
                return { "res" : self.convert(rs)['res'] }
            except Exception as e:
                return { "e" : e }
        elif self.is_textFile:
            try:
                # self.content.update("Extension":self.extension)
                return {"res" : self.content, "extention" : self.extension, "path" : self.fullpath}
            except Exception as e :
                return { "e" : e }


    def readUser(self): # version 1.0 consider 1 account in host
        try:
            col = "id"
            rs = self.db.execute("SELECT " + col + " FROM User limit 1")
            def parser(r): self.id = r[0]
            _.for_each(rs, parser)
            return { "res" : True }
        except Exception as e:
            return { "e" : e }
        
    def initDb(self, path):
        try:
            self.path = path
            self.conn = sqlite3.connect(path, check_same_thread=False )
            self.db = self.conn.cursor()
            return { "res" : True }
        except Exception as e:
            return { "e" : e }

    def initText(self,path):
        try:
            with open(path, 'r') as f:
                self.content = f.read()
            if self.debug: print(self.content)
        except Exception as e:
            print(e)

    def sync(self, notes):
        try:
            if not notes:
                print("is Empty")
                return { "res" : True }
            if not notes: return print("given 1 args(type=dict)")
            if not (type(notes) is dict): return print("args must be a dict")
            
            # question to user before processing sync 
            self.db.execute('DELETE FROM Note') # clean
            self.conn.commit()
            # insert format { Text, WindowPosition, Id, ParentId, Theme, CreatedAt, UpdatedAt }
            # self.readUser()
            self.temp = notes
            print("update")
            def parser(k):
                cols = ["Text", "WindowPosition", "Id", "ParentId", "Theme", "CreatedAt", "UpdatedAt"]
                parms = [self.temp[k]['Text'], self.temp[k]['WindowPosition'], uuid.uuid1(), self.id, self.temp[k]['Theme'], int(time.time()), int(time.time())]

                for index in range(0, len(parms)):
                    parms[index] = "'{0}'".format(parms[index])

                if self.debug:
                    for index in range(0, len(cols)):
                        print(cols[index], " = ", parms[index])
                
                sql = "INSERT INTO Note ({0}) VALUES ({1})".format(_.join(cols, ','), _.join(parms, ","))
                print("sql", sql)
                self.db.execute(sql)
                self.conn.commit()
            _.for_each(_.keys(notes), parser)
            print("sync")
            self.temp = None
            return { "res" : True }
        except Exception as e:
            print("{0} sync, check this {0}".format(__file__, e))
            return { "res" : False }
            
        
    def dumpBackupOneRow(self):
        try:
            col = ["*"]
            limit = "LIMIT 2" if self.debug else ''
            rs = self.db.execute("SELECT {0} FROM Note WHERE ParentId='{1}' {2}".format(_.join(col, ','), self.id, limit))
            self.backup = self.convert(rs)['res']
            return { "res" : True }
        except Exception as e:
            return { "e" : e }

    def convert(self, items):
        try:
            notes = {}
            def parser(r):
                self.noteCnt+=1
                notes.update({ str(self.noteCnt) : { "Text" : r[0], "WindowPosition" : r[1], "Theme" : r[2] } })

            _.for_each(items, parser)
            return { "res" : notes }
        except Exception as e:
            return { "e" : e }
        
if __name__ == '__main__':
    # msg += "# windows RS4 under version location is C:\\Users\\Username\\AppData\\Roaming\\Microsoft\\Sticky Notes\\StickyNotes.snt"
    # msg += "# ref http://pythonstudy.xyz/python/article/204-SQLite-%EC%82%AC%EC%9A%A9"
    # msg += "# Sample location"
    # msg += "# C:\\Users\\hdh09\\AppData\\Local\\Packages\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\\LocalState\\plum.sqlite"
    # msg += "# if update input type is string, using json parser"
    # msg += "# data = '{\"1\": {\"Text\": \"test\", \"WindowPosition\": \"V1NERgMAAAABAAAAAaoJAADcAQAAEgIAANcCAAAAAAA=\", \"Theme\": \"Yellow\"}}"
    # msg += "# dao.sync(json.loads(data))"
    # msg += "# dao.update(\"132\")"
    # msg += "\n"

    # print(msg)
    dao = DAO(fullpath="C:\\Users\\전인석\\Desktop\\SyncN.spec")
    print(dao.read())

    pass
