from sqlite3 import Connection
from typing import List, Self

from main.db.sql_statements import User as UserSql


class User:
    def __init__(self, username: str, user_id: str, author: str, insertion_time: float = None):
        self.created_at = insertion_time
        self.author = author
        self.user_id = user_id
        self.username = username

    def insert(self, con: Connection):
        cur = con.cursor()
        cur.execute(
            UserSql.insert_user,
            (self.username, self.user_id, self.author)
        )
        cur.close()

    @staticmethod
    def check_exists(con: Connection, usernaname: str) -> bool:
        cur = con.cursor()
        result = cur.execute(
            UserSql.select_check_user_exists,
            (usernaname,)
        ).fetchone()[0]
        cur.close()

        return False if result == 0 else True

    @staticmethod
    def get(con: Connection, usernaname: str) -> Self:
        cur = con.cursor()
        cur.execute(
            UserSql.select_user,
            (usernaname,)
        )
        result = cur.fetchone()
        cur.close()

        return User(*result)

    @staticmethod
    def get_several(con: Connection, usernames: List[str]) -> List[Self]:
        return [User.get(con, username) for username in usernames]
