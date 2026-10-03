import actions
import data


def input_int_validation(message: str) -> int:
    """Ask for an integer and repeat until the input is valid."""

    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def show_menu_welcoming() -> None:
    """Display the welcome message."""

    print("Welcome to the Student Control System!")


def show_menu() -> None:
    """Display the available menu options."""

    print(
        "\nPlease select an option:\n"
        "1. Add Student\n"
        "2. Show Students\n"
        "3. Top 3 Students\n"
        "4. General Average\n"
        "5. Export CSV\n"
        "6. Import CSV\n"
        "7. Exit\n"
        "8. Delete Student\n"
        "9. Show Failing Students"
    )


def get_menu_option() -> int:
    """Get a menu option from the user."""

    return input_int_validation(
        "What action would you like to perform? "
    )


def run_menu(student_list: list[dict]) -> None:
    """Run the main program loop."""

    while True:
        show_menu()

        option = get_menu_option()

        if option == 1:
            actions.add_student(student_list)

        elif option == 2:
            actions.show_students(student_list)

        elif option == 3:
            actions.show_top_students(student_list)

        elif option == 4:
            actions.show_general_average(student_list)

        elif option == 5:
            data.export_students(student_list)

        elif option == 6:
            imported_students = data.import_students()

            if imported_students is not None:
                student_list.clear()
                student_list.extend(imported_students)

        elif option == 7:
            print("Exiting the program.")
            break

        elif option == 8:
            actions.delete_student(student_list)

        elif option == 9:
            actions.show_failing_students(student_list)

        else:
            print("Invalid option. Please select a number from 1 to 9.")