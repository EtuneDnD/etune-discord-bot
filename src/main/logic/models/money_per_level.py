from sqlite3 import Connection
from typing import Self

from main.db.sql_statements import MoneyPerLevel as MoneyPerLevelSql


class MoneyPerLevel:
    def __init__(self, dictionary: dict[int, int]):
        self.dictionary = dictionary

    @staticmethod
    def select_all(connection: Connection) -> Self:
        cur = connection.cursor()
        cur.execute(MoneyPerLevelSql.select_all)
        result = dict(cur.fetchall())
        cur.close()
        return MoneyPerLevel(result)
