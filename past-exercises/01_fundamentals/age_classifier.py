# Program that asks for a name and age, then shows a personalized message.
# Age classification by range:
# Senior: 65 years or older
# Adult: 18 to 64 years
# Teenager: 13 to 17 years
# Child: 0 to 12 years

def validate_age():
    while True:
        try:
            age = int(input("Enter your age: "))
            if age < 0:
                print("Age cannot be negative. Please enter a valid age.")
            else:
                return age
        except ValueError:
            print("Please enter a valid number.")


def validate_name():
    while True:
        name = input("Enter your name: ").strip()
        if name == "":
            print("Name cannot be empty. Please enter a valid name.")
        else:
            return name


def classify_age(age):
    if age < 13:
        return "Child"
    elif age >= 65:
        return "Senior"
    elif age >= 18:
        return "Adult"
    else:
        return "Teenager"


def ask_again():
    while True:
        option = input("Do you want to enter another age? (y/n): ").lower()
        if option == 'y':
            run()
        elif option == 'n':
            print("Thank you for using the program. Goodbye!")
            break
        else:
            print("Invalid option. Please enter 'y' for yes or 'n' for no.")


def run():
    name = validate_name()
    age = validate_age()
    classification = classify_age(age)
    print(f"Hello {name}, your age classification is: {classification}")
    ask_again()


run()
