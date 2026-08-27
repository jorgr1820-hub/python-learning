import csv
import os


def export_students(student_list: list[dict]) -> None:
    """Export all students to a CSV file."""

    filename = "students.csv"

    if not student_list:
        print("There are no students to export.")
        return

    fieldnames = [
        "name",
        "section",
        "spanish",
        "english",
        "social_studies",
        "science",
    ]

    try:
        with open(
            filename,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
            )

            writer.writeheader()
            writer.writerows(student_list)

        print(f"Students exported successfully to {filename}.")

    except OSError as error:
        print(f"Error exporting students: {error}")


def import_students() -> list[dict] | None:
    """Import students from the CSV file."""

    filename = "students.csv"

    if not os.path.exists(filename):
        print("No previously exported CSV file was found.")
        return None

    students = []

    fieldnames = [
        "name",
        "section",
        "spanish",
        "english",
        "social_studies",
        "science",
    ]

    try:
        with open(
            filename,
            "r",
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.DictReader(file)

            if reader.fieldnames != fieldnames:
                print("The CSV file has an invalid format.")
                return None

            for row in reader:
                student = {
                    "name": row["name"],
                    "section": row["section"],
                    "spanish": int(row["spanish"]),
                    "english": int(row["english"]),
                    "social_studies": int(row["social_studies"]),
                    "science": int(row["science"]),
                }

                students.append(student)

        print("Students imported successfully.")
        return students

    except (OSError, ValueError, KeyError) as error:
        print(f"Error importing students: {error}")
        return None