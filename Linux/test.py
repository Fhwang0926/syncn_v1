import itertools, numpy

a = {1:"a",2:'b',3:'c',4:'d',5:'e'}
b = {2:'b', 6:'f', 8:'t', 4:'d'}
print(a.update(b))
mat = list(set(a)&set(b))
mismat = list(set(a)^set(b))
print(mat)
c = {}
# c = [a[mat] for x in mat]
for i in (mat+mismat):
    c.update({i:t[i]})
print(c)


