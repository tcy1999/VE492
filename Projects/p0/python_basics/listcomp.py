nums = [1, 2, 3, 4, 5, 6]
plusOneNums = [x + 1 for x in nums]
print(plusOneNums)
print(list(map(lambda x: x + 1, nums)))
oddNums = [x for x in nums if x % 2 == 1]
print(oddNums)
oddNumsPlusOne = [x + 1 for x in nums if x % 2 == 1]
print(oddNumsPlusOne)
