import itertools

a = [1,2,3,4,5]
b = [1,4,5,6,8]

result = list(zip(a,b))
print(result[0])
# print(list(zip(a,b)))
# result = itertools.combinations(a,b)
# print(result)

# compare = map(lambda (i,j): i==j,zip(a,b))
compare = [i == j for (i,j) in itertools.product(a,b)]
print(compare)
compare2 = [i == j for (i,j) in list(zip(a,b))]
print(compare2)

print(itertools.combinations(a,b)[compare])