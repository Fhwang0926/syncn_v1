import sqlite3
import PathSearch
# import pydash as _
import uuid
#windows RS4 under version location is C: \Users\Username\AppData\Roaming\Microsoft\Sticky Notes\StickyNotes.snt


class noteSql():
    def __init__(self):
        self.fullpath = PathSearch.SetPath().result
        self.path = ''
        self.cursor = None
        self.conn = None
        self.build(self.fullpath)
        pass

    def read(self, chk=False):
        col = "WindowPosition, Theme, Id, ParentId" if chk else "Text, WindowPosition, Theme"
        rs = self.cursor.execute("SELECT " + col + " FROM Note")
        rs_array = []
        for row in rs:
            rs_array.append(row)
            if(chk):
                break
        return self.convert(rs_array, chk)

    def build(self, path):
        self.path = path
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        pass

    def update(self):
        # db.execute('update note set  = ? where t1 = ?', (row['i1'], row['t1']))
        # db.commit()
        pass

    def convert(self, items, chk):
        notes = {}
        cnt = 1
        i = None
        for item in items:
            if(chk):
                i = {str(cnt): {
                    "WindowPosition": item[0], "Theme": item[1], "Id": item[2], "ParentId": item[3]}}
            else:
                i = {
                    str(cnt): {"Text": item[0], "WindowPosition": item[1], "Theme": item[2]}}
            notes.update(i)
            cnt += 1
        return notes

    def check(self):
        return self.read(chk=True)

# SELECT * FROM note

if __name__ == '__main__':
    pass
