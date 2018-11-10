def generate_nums():
    num = 0
    while True:
        yield num
        num = num + 1


nums = generate_nums()

print(next(nums))
print(next(nums))
print(next(nums))
# for x in nums:
#     print(x)
#
#     if x > 9:
#         break

