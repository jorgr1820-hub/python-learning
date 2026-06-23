#This program return the total of "one + two 

def add_nums(num_one , num_two):
    global three
    three = 5
    return num_one + num_two + three


one = int(input("Enter #1:"))
two = int(input("Enter #2:"))
three = 8

print(f"this is {add_nums(one,two)}")
