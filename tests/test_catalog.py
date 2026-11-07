import pytest
from classrooms.models import Classroom
from classrooms.catalog import Catalog
from classrooms.exceptions import DuplicateIdError, NotFoundError, InvalidEntityError, CorruptedFileError, UnsupportedVersionError

# Создание допустимой сущности
def test_create_valid_classroom():
    room = Classroom(
        id = "1",
        name = "IT-1",
        category = "seminars",
        year = 2023,
        area = 80,
        number_of_seats = 45
    )

    assert room.id == "1"
    assert room.name == "IT-1"

# Создание недопустимой сущности
def test_create_invalid_classroom():
    with pytest.raises(InvalidEntityError):  # или ваш InvalidEntityError
        Classroom(
            id="",
            name="IT-1",
            category="seminars",
            year=2023,
            area=80,
            number_of_seats=45
        )

# Добавление и получение данных
def test_add_and_get():
    catalog = Catalog()
    room = Classroom("1", "IT-1", "seminars", 2023, 80, 45)
    catalog.add(room)

    assert len(catalog) == 1
    assert catalog.get("1") is room

# Удаление сущности из каталога
def test_remove():
    catalog = Catalog()
    room = Classroom("1", "IT-1", "seminars", 2023, 80, 45)
    catalog.add(room)
    catalog.remove(room.id)

    assert len(catalog) == 0

# Добавление сущностей с одинаковым id (недопустимо)
def test_duplicate_id():
    catalog = Catalog()
    room = Classroom("1", "IT-1", "seminars", 2023, 80, 45)
    catalog.add(room)

    with pytest.raises(DuplicateIdError):
        room = Classroom("1", "IT-2", "seminars", 2020, 100, 60)
        catalog.add(room)

# Поиск сущностей по категории
def test_find_by_category_and_name():
    catalog = Catalog()
    catalog.add(Classroom("1", "IT-1", "lectures", 2017, 120, 280))
    catalog.add(Classroom("2", "it-1", "seminars", 2019, 80, 240))
    catalog.add(Classroom("3", "IT-3", "lectures", 2020, 200, 200))

    lectures = catalog.find_by_category("lectures")
    assert len(lectures) == 2

    result = catalog.find_by_name("it-1")
    assert len(result) == 2

# Порядок итерации объекта каталога
def test_iteration_order():
    catalog = Catalog()
    catalog.add(Classroom("1", "IT-1", "lectures", 2017, 120, 280))
    catalog.add(Classroom("2", "it-1", "seminars", 2019, 80, 240))
    catalog.add(Classroom("3", "IT-3", "lectures", 2020, 200, 200))

    ids = [room.id for room in catalog]
    assert ids == sorted(ids)

# Сохранение и загрузка данных
def test_json_round_trip(tmp_path):
    catalog = Catalog()
    room = Classroom("2", "it-1", "seminars", 2019, 80, 240)
    catalog.add(room)

    path = tmp_path / "test.json"
    catalog.save(path)

    new_catalog = Catalog()
    new_catalog.load(path)

    assert len(new_catalog) == 1
    loaded = new_catalog.get("2")
    assert loaded.name == room.name
    assert loaded.area == room.area

# Поврежденный json + неизвестная версия конфига
def test_corrupted_json_and_unknown_version(tmp_path):
    catalog = Catalog()
    catalog.add(Classroom("2", "it-1", "seminars", 2019, 80, 240))

    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{ это не json", encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        catalog.load(bad_path)

    version_path = tmp_path / "version.json"
    version_path.write_text('{"format_version": 999, "items": []}', encoding="utf-8")
    with pytest.raises(UnsupportedVersionError):
        catalog.load(version_path)

# Проверка отсутствия частичного изменения после ошибки загрузки
def test_atomic_load(tmp_path):
    catalog = Catalog()
    original = Classroom("1", "it-1", "seminars", 2019, 80, 240)
    catalog.add(original)

    # файл, который сломается в середине (невалидная сущность)
    path = tmp_path / "partial.json"
    path.write_text('''
    {
      "format_version": 1,
      "items": [
        {"id": "Б-201", "name": "Нормальная", "category": "лекционная", "year": 2020, "capacity": 50, "floor": 2},
        {"id": "", "name": "Битая", "category": "лекционная", "year": 2020, "capacity": 50, "floor": 2}
      ]
    }
    ''', encoding="utf-8")

    with pytest.raises(CorruptedFileError):
        catalog.load(path)

    # каталог не должен измениться
    assert len(catalog) == 1
    assert catalog.get("1").name == "it-1"