"""Entry point: owns the roster and hands control over to the menu."""

import menu
from model import Student

student_list: list[Student] = []


def main() -> None:
    """Greet the user and run the menu loop.

    The roster is held in memory for the session only; it is not persisted
    between runs.
    """
    menu.show_menu_welcoming()
    menu.run_menu(student_list)


if __name__ == "__main__":
    main()
