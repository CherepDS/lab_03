import time
from classrooms.catalog import Catalog
from classrooms.models import Classroom

# Краткая демонстрация функционала

def main():
    catalog = Catalog()

    # Создание и добавление
    room1 = Classroom("А-101", "Лекционная", "лекционная", 2015, 80, 1)
    room2 = Classroom("Б-202", "Компьютерный класс", "лабораторная", 2018, 25, 2)
    room3 = Classroom("А-103", "Семинарская", "семинарская", 2020, 30, 1)

    catalog.add(room1)
    catalog.add(room2)
    catalog.add(room3)
    print(f"Добавлено аудиторий: {len(catalog)}")

    # Получение
    print("Получена:", catalog.get("А-101").name)

    # Поиск
    print("Лекционные:", [r.id for r in catalog.find_by_category("лекционная")])
    print("Поиск по имени 'класс':", [r.name for r in catalog.find_by_name("класс")])

    # Итерация
    print("Все аудитории (по id):")
    for room in catalog:
        print(f"  {room.id} — {room.name}")

    # Проверка наличия
    print("А-101 в каталоге:", "А-101" in catalog)

    # Сохранение и загрузка
    catalog.save("demo.json")
    new_catalog = Catalog()
    new_catalog.load("demo.json")
    print(f"После загрузки: {len(new_catalog)} аудиторий")

    # Удаление
    catalog.remove("Б-202")
    print(f"После удаления: {len(catalog)}")

if __name__ == "__main__":
    main()