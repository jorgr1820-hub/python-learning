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

def multiply_nums(a,b):
    return a * b 

def divide_nums(a,b):
    return a / b


def main_operator():
    nums_a = 10
    nums_b = 0
    decision = 0
    print("Select the operation and enter 1 number")
    while decision < 1 or decision > 4:
        print("Select the operation by number")
        decision = get_int("1-sum | 2-substract | 3-multiply | 4-divide: \n")
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
                    result = multiply_nums(nums_a,nums_b)
                    break
                else:
                    result = divide_nums(nums_a,nums_b)
                    break        
            except ZeroDivisionError as error:
                print(f"Can not divide by 0. Try again{error}")
    nums_b = re            
    print(f"The result is {result}")
    continue_decision = input("Do you want to continue? (yes/no): ")
    if continue_decision.lower().strip() == 'yes':
        main_operator()


main_operator()