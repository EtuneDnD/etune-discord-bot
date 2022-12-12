from typing import Self
from sqlite3 import Cursor
from db.sql_statements import Character as character_sql_statements


class Character:
    def __init__(self, character_name: str, level: int, username: str, author: str, insertion_time=None):
        self.character_name = character_name
        self.level = level
        self.username = username
        self.author = author
        self.insertion_time = insertion_time

    def insert_character(self, cur: Cursor):
        cur.execute(
            character_sql_statements.insert_character,
            (
                self.character_name,
                self.level,
                self.username,
                self.author
            )
        )

    @staticmethod
    def check_character_exists(cur: Cursor, character_name: str):
        cur.execute(
            character_sql_statements.select_check_character_exists,
            (character_name,)
        )

        return False if cur.fetchone()[0] == 0 else True

    @staticmethod
    def get_characters_by_username(cur: Cursor, username: str):
        cur.execute(
            character_sql_statements.select_user_characters,
            (username,)
        )

        result = cur.fetchall()

        return [
            Character(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4]) for tupla in result
        ]

    @staticmethod
    def get_character_by_character_name(cur: Cursor, character_name: str) -> Self:
        cur.execute(
            character_sql_statements.select_character_by_character_name,
            (character_name,)
        )

        result = cur.fetchone()

        return Character(result[0], result[1], result[2], result[3], result[4])

    @staticmethod
    def get_characters_by_character_names(cur: Cursor, characters: list[str]) -> list[Self]:
        return [Character.get_character_by_character_name(cur, character) for character in characters]
