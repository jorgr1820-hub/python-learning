def get_int(message):
    while True:
        try:
            return int(input(message))
        except ValueError as error:
            print(f"Wrong value! Try again. {error}")


def add_nums(a, b):
    return a + b


def substrac_nums(a, b):
    return a - b


def multiply_nums(a, b):
    return a * b


def divide_nums(a, b):
    return a / b


def delete_nums(result):
    previous_result = result
    result = 0
    print("The operator selected was 5-Delete")
    print(f"Previous result: {previous_result}")
    print("The result has been cleared")
    return result


def operations(decision, current_result):
    while True:
        try:
            num = get_int("Enter value: ")

            if decision == 1:
                print("The operator selected was 1-Sum")
                return add_nums(current_result, num)
            elif decision == 2:
                print("The operator selected was 2-Subtract")
                return substrac_nums(current_result, num)
            elif decision == 3:
                print("The operator selected was 3-Multiply")
                return multiply_nums(current_result, num)
            elif decision == 4:
                print("The operator selected was 4-Divide")
                return divide_nums(current_result, num)

        except ZeroDivisionError as error:
            print(f"Cannot divide by 0. Try again. {error}")


def main_operator():
    current_result = 0

    while True:
        if current_result >= 1:
            print(f"\nCurrent result: {current_result}")
        print("\nSelect the operation you want to perform:")

        decision = get_int("\n1- Sum | 2- Subtract | 3- Multiply | 4- Divide | 5- Delete | 6- Exit: ")

        if decision in [1, 2, 3, 4]:
            current_result = operations(decision, current_result)
            print(f"\nNew result: {current_result}")

        elif decision == 5:
            current_result = delete_nums(current_result)

        elif decision == 6:
            print("The operator selected was 6-Exit")
            print("Good bye!")
            break

        else:
            print("Invalid option. Please try again.")


main_operator()