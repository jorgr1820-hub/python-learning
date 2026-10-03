from model import Student


def add_student(student_list: list[Student]) -> None:
    """Prompt for student information and add the student to the roster."""

    while True:
        name = get_valid_name()
        section = get_valid_section()

        if not student_exists(student_list, name, section):
            break

        print("Student already exists in the roster.")

    spanish = get_valid_grade("Spanish")
    english = get_valid_grade("English")
    social_studies = get_valid_grade("Social Studies")
    science = get_valid_grade("Science")

    student = Student(
        name,
        section,
        spanish,
        english,
        social_studies,
        science,
    )

    student_list.append(student)

    print("Student added successfully.")


def get_valid_name() -> str:
    """Ask for a student's name until a valid name is provided."""

    while True:
        name = input("Enter student's full name: ")

        if is_valid_name(name):
            return name.strip()

        print("Invalid name. Please try again.")


def is_valid_name(name: str) -> bool:
    """Return True when the name contains only valid characters."""

    if not name.strip():
        return False

    for char in name:
        if not (char.isalpha() or char.isspace() or char == "-"):
            return False

    return True


def get_valid_section() -> str:
    """Ask for a student's section until a valid section is provided."""

    while True:
        section = input("Enter student's section: ")

        if is_valid_section(section):
            return section.strip().upper()

        print("Invalid section. Use the format 11B.")


def is_valid_section(section: str) -> bool:
    """Return True for sections using digit-digit-letter format."""

    section = section.strip()

    if len(section) != 3:
        return False

    if not section[:2].isdigit():
        return False

    if not section[2].isalpha():
        return False

    return True


def get_valid_grade(subject: str) -> int:
    """Ask for a grade until an integer between 0 and 100 is provided."""

    while True:
        grade = input_int_validation(
            f"Enter student's {subject} grade (0-100): "
        )

        if 0 <= grade <= 100:
            return grade

        print("Invalid grade. Please enter a value between 0 and 100.")


def input_int_validation(message: str) -> int:
    """Ask for an integer and repeat until the input is valid."""

    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def student_exists(
    student_list: list[Student],
    name: str,
    section: str,
) -> bool:
    """Return True if a student with the same name and section exists."""

    for student in student_list:
        if (
            student.name.lower() == name.lower()
            and student.section.upper() == section.upper()
        ):
            return True

    return False


def calculate_average(student: Student) -> float:
    """Calculate the average grade for a student."""

    total = (
        student.spanish
        + student.english
        + student.social_studies
        + student.science
    )

    return total / 4


def show_students(student_list: list[Student]) -> None:
    """Display all students and their information."""

    if not student_list:
        print("There are no students in the roster.")
        return

    print("\n--- Students ---")

    for student in student_list:
        average = calculate_average(student)

        print(f"Name: {student.name}")
        print(f"Section: {student.section}")
        print(f"Spanish: {student.spanish}")
        print(f"English: {student.english}")
        print(f"Social Studies: {student.social_studies}")
        print(f"Science: {student.science}")
        print(f"Average: {average:.2f}")
        print("--------------------")


def show_top_students(student_list: list[Student]) -> None:
    """Display the top three students by average grade."""

    if not student_list:
        print("There are no students in the roster.")
        return

    sorted_students = sorted(
        student_list,
        key=calculate_average,
        reverse=True,
    )

    top_students = sorted_students[:3]

    print("\n--- Top Students ---")

    for position, student in enumerate(top_students, start=1):
        average = calculate_average(student)

        print(
            f"{position}. {student.name} "
            f"- {student.section} "
            f"- Average: {average:.2f}"
        )


def show_general_average(student_list: list[Student]) -> None:
    """Display the average grade across all students."""

    if not student_list:
        print("There are no students in the roster.")
        return

    total_average = 0

    for student in student_list:
        total_average += calculate_average(student)

    general_average = total_average / len(student_list)

    print(f"General average: {general_average:.2f}")


def delete_student(student_list: list[Student]) -> None:
    """Delete a student after confirming with the user."""

    if not student_list:
        print("There are no students in the roster.")
        return

    name = get_valid_name()
    section = get_valid_section()

    for student in student_list:
        if (
            student.name.lower() == name.lower()
            and student.section.upper() == section.upper()
        ):
            print(
                f"Student found: {student.name} "
                f"- {student.section}"
            )

            confirmation = input(
                "Are you sure you want to delete this student? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                student_list.remove(student)
                print("Student deleted successfully.")
            else:
                print("Deletion cancelled.")

            return

    print("Student not found.")


def show_failing_students(student_list: list[Student]) -> None:
    """Display students with at least one grade below 60."""

    if not student_list:
        print("There are no students in the roster.")
        return

    found_failing_student = False

    print("\n--- Failing Students ---")

    for student in student_list:
        failed_subjects = get_failed_subjects(student)

        if failed_subjects:
            found_failing_student = True

            print(f"Name: {student.name}")
            print(f"Section: {student.section}")

            for subject, grade in failed_subjects:
                print(f"{subject}: {grade}")

            print("--------------------")

    if not found_failing_student:
        print("There are no failing students.")


def get_failed_subjects(
    student: Student,
) -> list[tuple[str, int]]:
    """Return all subjects with grades below 60."""

    subjects = {
        "Spanish": student.spanish,
        "English": student.english,
        "Social Studies": student.social_studies,
        "Science": student.science,
    }

    failed_subjects = []

    for subject, grade in subjects.items():
        if grade < 60:
            failed_subjects.append((subject, grade))

    return failed_subjects



