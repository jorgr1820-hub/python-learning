class Student:
    """Represent a student and their grades.

    The class owns the translation between the object and the plain dict
    that the CSV layer needs. Nothing else in the program should know the
    shape of a student row.
    """

    # Contrato con el CSV: nombre y orden de las columnas.
    FIELDS = (
        "name",
        "section",
        "spanish",
        "english",
        "social_studies",
        "science",
    )

    def __init__(
        self,
        name: str,
        section: str,
        spanish: int,
        english: int,
        social_studies: int,
        science: int,
    ):
        self.name = name
        self.section = section
        self.spanish = spanish
        self.english = english
        self.social_studies = social_studies
        self.science = science

    def to_dict(self) -> dict:
        """Return the student as a plain dict, ready for csv.DictWriter."""

        return {
            "name": self.name,
            "section": self.section,
            "spanish": self.spanish,
            "english": self.english,
            "social_studies": self.social_studies,
            "science": self.science,
        }

    @classmethod
    def from_dict(cls, row: dict) -> "Student":
        """Build a Student from a CSV row.

        Every value read from a CSV arrives as text, so grades are
        converted back to int here. A bad value raises ValueError and the
        data layer reports it.
        """

        return cls(
            name=row["name"],
            section=row["section"],
            spanish=int(row["spanish"]),
            english=int(row["english"]),
            social_studies=int(row["social_studies"]),
            science=int(row["science"]),
        )
