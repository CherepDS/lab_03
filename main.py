from classrooms.catalog import Catalog
from classrooms.models import Classroom

def find_by_category_and_name():
    catalog = Catalog()
    catalog.add(Classroom("1", "IT-1", "lectures", 2017, 120, 280))
    catalog.add(Classroom("2", "it-1", "seminars", 2019, 80, 240))
    catalog.add(Classroom("3", "IT-3", "lectures", 2020, 200, 200))

    lectures = catalog.find_by_category("lectures")
    print(len(lectures))

    result = catalog.find_by_name("it-1")
    print(len(result))
    print(all("2" in r.name.lower() for r in result))

find_by_category_and_name()