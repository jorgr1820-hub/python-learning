# Print from 1 to 10 using range.
# Print from 10 to 1 using range with a negative step.
# Print only even numbers from 0 to 20.
# Given a string s = "Pizza con piña", print the indexes and characters: 0:P, 1:i, ...


for index in range(10 + 1):
    print(f"Here are the range from 1 to 10 {index}")



for index in range(-1, -11, -1):
    print(f"Here are the range from 1 to 10 {index}")


for index in range(1,20):
    if index % 2 == 0:
        even = index
        print(even)


s = "Pizza con piña"
indexes = [0,1]
for i in indexes:
    print(f"{i}:{s[i]}")
