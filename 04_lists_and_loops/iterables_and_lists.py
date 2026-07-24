first_list = ["There", "are", "cases", "where", "iterating", "by"]
second_list = ["cases", "where", "iteration", "by", "index", "is"]

for index in range(len(first_list)):
    print(first_list[index], second_list[index])


my_string = "Pizza con piña"

for index in range(len(my_string) - 1, -1, -1):
    print(my_string[index])


my_list = [4, 3, 6, 1, 7]
my_list[0], my_list[-1] = my_list[-1], my_list[0]
print(my_list)


my_list = [4, 3, 6, 1, 7]

for index in range(len(my_list) - 1, -1, -1):
    if my_list[index] % 2 != 0:
        my_list.pop(index)

print(my_list)

my_list = []
number = 0
for index in range(1,11):
    number = int(input(f"Enter the number #{index}: "))
    my_list.append(number)
print(f"Your list is {my_list}")
print(f"The highest number is: {max(my_list)}")
