import itertools, numpy

a = [1,2,3,4,5]
b = [1,4,5,6,8]


# result = list(zip(a,b))
# print(result[0])
# print(list(zip(a,b)))
# result = itertools.combinations(a,b)
# print(result)

# compare = map(lambda (i,j): i==j,zip(a,b))
item = list(itertools.product(a,b))
compare = [i == j for (i,j) in item]
print(compare)
# compare2 = [i == j for (i,j) in list(zip(a,b))]
# print(compare2)

print(item)
source = list(itertools.compress(item, compare))
print(source)
#
# print(list(set(a).intersection(b)))
# print(set(a+b))

result = list(set(a+b))
for i in result:
    for j in source:
        if j[0] == i:
            result.remove(i)
            break
        else:
            continue

print()
print(a+b)
print(result)