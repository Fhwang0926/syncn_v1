import string, random, sys

randomName = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
print(randomName)