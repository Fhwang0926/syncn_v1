import string, random, sys


a = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
b = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

print(a)
print(b)


