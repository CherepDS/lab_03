# Базовый класс CatalogError + отдельные ошибки

class CatalogError(Exception):
    """Базовое исключение каталога."""
    pass

class InvalidEntityError(CatalogError):
    """Неверная сущность (нарушены инварианты)."""
    pass

class DuplicateIdError(CatalogError):
    """Попытка добавить объект с уже существующим id."""
    pass

class NotFoundError(CatalogError):
    """Объект с указанным id не найден."""
    pass

class UnsupportedVersionError(CatalogError):
    """Неподдерживаемая версия формата файла."""
    pass

class CorruptedFileError(CatalogError):
    """Файл повреждён или имеет неверный формат."""
    pass