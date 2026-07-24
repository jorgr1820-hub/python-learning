# Lists + loops + find minimum without min()

# Given nums = [4, -2, 7, 0], find the lowest using a loop (includes negatives and 0).

# Find the highest without max().

# Count how many are positive, negative, and zero (using 3 counters, no extra lists).

# Calculate the average without using libraries.

nums = [4, -2, 7, ]
num_lowest = nums[0]
num_highest = nums[0]
for index in nums:
    if index < num_lowest:
        num_lowest = index
    elif index > num_highest:
        num_highest = index


positive = 0
negative = 0
zeros = 0
for x in nums:
    if x == 0:
        zeros += 1
    elif x > 0:
        positive += 1
    else:
        negative += 1


total = 0
for t in nums:
    total += t


average = total / len(nums)


print(f"The lowest number is: {num_lowest} and the highest is: {num_highest}")
print(f"The total of positive is: {positive}")
print(f"The total of negative is: {negative}")
print(f"The total of zeros is: {zeros}")
print(f"The average is: {average}")
