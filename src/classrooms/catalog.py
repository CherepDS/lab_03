import json
from classrooms.models import Classroom
from classrooms.exceptions import NotFoundError, DuplicateIdError, CorruptedFileError, UnsupportedVersionError, InvalidEntityError

# Класс каталога
class Catalog:
    def __init__(self):
        self._items: dict[str, Classroom] = {}

    def __len__(self) -> int:
        return len(self._items)

    def __contains__(self, item_id: str) -> bool:
        return item_id in self._items

    def __iter__(self):
        # Порядок итерации: по возрастанию
        for item_id in sorted(self._items):
            yield self._items[item_id]

    # Добавление объекта аудитории в каталог
    def add(self, item: Classroom) -> None:
        if item.id in self._items:
            raise DuplicateIdError(f"Аудитория с id '{item.id}' уже существует")
        self._items[item.id] = item

    # Получение объекта аудитории по его id
    def get(self, item_id: str) -> Classroom:
        if item_id not in self._items:
            raise NotFoundError(f"Аудитория с id '{item_id}' не найдена")
        return self._items[item_id]

    # Получение всех объектов аудиторий с заданной категорией
    def find_by_category(self, category: str) -> list[Classroom]:
        return [item for item in self._items.values() if item.category.lower() == category.lower()]

    # Получение всех объектов аудиторий с заданным именем
    def find_by_name(self, name: str) -> list[Classroom]:
        return [item for item in self._items.values() if item.name.lower() == name.lower()]

    # Удаление объекта аудитории из каталога
    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise NotFoundError(f"Аудитория с id '{item_id}' не найдена")
        del self._items[item_id]

    # Сохранение каталога в формате json
    def save(self, path: str = "catalog.json") -> None:
        data = {
            "format_version": 1,
            "items": [
                {
                    "id": item.id,
                    "name": item.name,
                    "category": item.category,
                    "year": item.year,
                    "area": item.area,
                    "number_of_seats": item.number_of_seats,
                }
                for item in self._items.values()
            ]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Создание каталога с помощью json конфига
    def load(self, path: str) -> None:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            raise CorruptedFileError("Файл повреждён или не читается")

        if data.get("format_version") != 1:
            raise UnsupportedVersionError("Неподдерживаемая версия формата")

        # Сначала собираем всё во временный словарь
        new_items = {}
        try:
            for raw in data.get("items", []):
                room = Classroom(**raw)  # здесь сработают инварианты
                if room.id in new_items:
                    raise DuplicateIdError(f"Аудитория с id '{room.id}' уже существует")
                new_items[room.id] = room
        except (TypeError, KeyError, InvalidEntityError, DuplicateIdError):
            raise CorruptedFileError("Некорректные данные в файле")

        # Только если всё прошло успешно — заменяем содержимое
        self._items = new_items