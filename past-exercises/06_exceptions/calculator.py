def get_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError as error:
            print(f"Wrong Value! Try again{error}")


def add_nums(a,b):
    return a + b 


def substrac_nums(a,b):
    return a - b 


def miltiply_nums(a,b):
    return a * b 


def divide_nums(a,b):
    return a / b


print("Select the operation and enter 1 numbers")
nums_a = 0
nums_b = 2
decision = 0
while decision < 1 or decision > 4:
    print("Select the operation by number")
    decision = get_int("1-Sum | 2-Substract | 3-Multiply | 4-Divide: \n")
    if decision < 1 or decision > 4:
        print("Error! Value must be between 1-4")
    while True:
        try:
            nums_a = get_int("Enter Value:")
            result = 0 
            if decision == 1:
                result = add_nums(nums_a,nums_b)
                break
            elif decision == 2:
                result = substrac_nums(nums_a,nums_b)
                break
            elif decision == 3:
                result = miltiply_nums(nums_a,nums_b)
                break
            else:
                result = divide_nums(nums_a,nums_b)
                break        
        except ZeroDivisionError as error:
            print(f"Can not divide by 0. Try again{error}")
    print(f"The result is {result}")
    continue_decision = input("Do you want to continue? (y/n): ")
    if continue_decision.lower() != 'y':
        break   
