import os
import re

# It will be executed search.py
path = os.environ['HOME'] + "/.config/xpad"

files = []
for (dirpath, dirname, filename) in os.walk(path):
    files = filename

# It will be executed core.py
#r = re.compile("^[content]+[-]+[a-zA-Z0-9]")
#contentFile = list(filter(r.search, files))
r = re.compile("^[info]+[-]+[a-zA-Z0-9]")
infoFile = list(filter(r.search, files))

#print(contentFile)

# It will be returned new .py file
result = {}
with open(path + "/" + infoFile[0], "r") as f:
    contentName = f.readlines()[-1].split()[1]
    f.seek(0)
    with open(path + "/" + contentName) as ff:
        result.update({"data":ff.read()})
    result.update({"info":f.read()})
    result.update({"content":contentName})
print(result)
#print(files)
