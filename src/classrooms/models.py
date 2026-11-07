from dataclasses import dataclass
from classrooms.exceptions import InvalidEntityError

@dataclass
class Classroom:
    id: str
    name: str
    category: str
    year: int
    area: int
    number_of_seats: int

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise InvalidEntityError("ID не может быть пустым!")

        if not self.name or not self.name.strip():
            raise InvalidEntityError("Название не может быть пустым!")

        if not self.category or not self.category.strip():
            raise InvalidEntityError("Категория не может быть пустой!")

        if self.year < 1900 or self.year > 2026:
            raise InvalidEntityError("Некорректный год!")

        if self.area <= 0:
            raise InvalidEntityError("Площадь должна быть положительным числом!")

        if self.number_of_seats < 0:
            raise InvalidEntityError("Количество мест не может быть отрицательным!")