from sqlite3 import Cursor
from typing import List, Self

from main.db.sql_statements import User as UserSql


class User:
    def __init__(self, username: str, user_id: str, author: str, insertion_time: float = None):
        self.insertion_time = insertion_time
        self.author = author
        self.user_id = user_id
        self.username = username

    def insert(self, cur: Cursor):
        cur.execute(
            UserSql.insert_user,
            (self.username, self.user_id, self.author)
        )

    @staticmethod
    def check_exists(cur: Cursor, usernaname: str) -> bool:
        cur.execute(
            UserSql.select_check_user_exists,
            (usernaname,)
        )

        return False if cur.fetchone()[0] == 0 else True

    @staticmethod
    def get(cur: Cursor, usernaname: str) -> Self:
        cur.execute(
            UserSql.select_user,
            (usernaname,)
        )

        result = cur.fetchone()

        return User(result[0], result[1], result[2], result[3])

    @staticmethod
    def get_several(cur: Cursor, usernames: List[str]) -> List[Self]:
        return [User.get(cur, username) for username in usernames]
