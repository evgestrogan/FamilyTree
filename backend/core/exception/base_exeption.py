from sqlalchemy.exc import IntegrityError


class UniqueIndexException(Exception):
    """Обработка занесения значения в базу данных уникального значения"""

    def __init__(self, exc: IntegrityError):
        self.message = exc.args[0][exc.args[0].find(':'):exc.args[0].find('DETAIL')]
        self.detail = exc.detail
        super().__init__(self.detail, self.message)


class ForeignKeyErrorException(Exception):
    """Обработка занесения значения в базу данных с неправильным внешник ключлм"""

    def __init__(self, exc: IntegrityError):
        self.message = exc.args[0][exc.args[0].find(':'):exc.args[0].find('DETAIL')]
        self.detail = exc.detail
        super().__init__(self.detail, self.message)