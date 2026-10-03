import csv
import os

from model import Student

FILENAME = "students.csv"


def export_students(student_list: list[Student]) -> None:
    """Export all students to a CSV file."""

    if not student_list:
        print("There are no students to export.")
        return

    try:
        with open(
            FILENAME,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(Student.FIELDS),
            )

            writer.writeheader()

            for student in student_list:
                writer.writerow(student.to_dict())

        print(f"Students exported successfully to {FILENAME}.")

    except OSError as error:
        print(f"Error exporting students: {error}")


def import_students() -> list[Student] | None:
    """Import students from the CSV file."""

    if not os.path.exists(FILENAME):
        print("No previously exported CSV file was found.")
        return None

    students = []

    try:
        with open(
            FILENAME,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != list(Student.FIELDS):
                print("The CSV file has an invalid format.")
                return None

            for row in reader:
                students.append(Student.from_dict(row))

        print("Students imported successfully.")
        return students

    except (OSError, ValueError, KeyError) as error:
        print(f"Error importing students: {error}")
        return None
