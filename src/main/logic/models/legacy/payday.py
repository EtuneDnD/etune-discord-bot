from sqlite3 import Connection
from typing import Optional

from main.db.sql_statements import Payday as PaydaySql


class Payday:
    def __init__(self, username: str, claimed: bool, author: str, insertion_time: Optional[str] = None):
        self.insertion_time = insertion_time
        self.author = author
        self.claimed = claimed
        self.username = username

    @staticmethod
    def set_claimed(connection: Connection, username: str) -> None:
        cur = connection.cursor()
        cur.execute(
            PaydaySql.update_payday_claim,
            (username,)
        )
        cur.close()

    def insert_new_claimer(self, connection: Connection) -> None:
        cur = connection.cursor()
        cur.execute(
            PaydaySql.insert_new_claimer,
            (self.username, self.claimed, self.author)
        )
        cur.close()

    @staticmethod
    def check_claimer_exists(connection: Connection, username: str) -> bool:
        cur = connection.cursor()
        cur.execute(
            PaydaySql.select_payday_check_exists,
            (username,)
        )

        result = cur.fetchone()[0]
        cur.close()

        return False if result == 0 else True

    @staticmethod
    def check_claimed(connection: Connection, username: str) -> bool:
        cur = connection.cursor()
        cur.execute(
            PaydaySql.select_payday_check_claimed,
            (username,)
        )
        result = cur.fetchone()[0]
        cur.close()
        return True if result == 1 else False
