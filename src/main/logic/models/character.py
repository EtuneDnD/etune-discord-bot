from sqlite3 import Connection
from typing import Self

from main.db.sql_statements import Character as RewardSql


class Character:
    def __init__(self, name: str, level: int, username: str, author: str, insertion_time=None,
                 actor_base64: str = None, *args):
        self.name = name.lower()
        self.level = level
        self.username = username
        self.author = author
        self.insertion_time = insertion_time
        self.actor_base64 = actor_base64

    def insert_character(self, connection: Connection) -> None:
        cur = connection.cursor()
        cur.execute(
            RewardSql.insert_character,
            (
                self.name,
                self.level,
                self.username,
                self.author
            )
        )
        cur.close()

    def update(self, connection: Connection) -> None:
        cur = connection.cursor()
        cur.execute(
            RewardSql.update_character,
            (
                self.level,
                self.username,
                self.author,
                self.actor_base64,
                self.name
            )
        )
        cur.close()

    @staticmethod
    def check_character_exists(connection: Connection, character_name: str) -> bool:
        character_name = character_name.lower()
        cur = connection.cursor()
        cur.execute(
            RewardSql.select_check_character_exists,
            (character_name,)
        )

        result = cur.fetchone()[0]
        cur.close()

        return False if result == 0 else True

    @staticmethod
    def check_characters_exist(connection: Connection, character_names: list[str]) -> bool:
        for character_name in character_names:
            if not Character.check_character_exists(connection, character_name):
                return False
        return True

    @staticmethod
    def get_characters_by_username(connection: Connection, username: str) -> list[Self]:
        cur = connection.cursor()
        cur.execute(
            RewardSql.select_user_characters,
            (username,)
        )

        result = cur.fetchall()
        cur.close()

        return [Character(*tupla) for tupla in result]

    @staticmethod
    def get_character_by_character_name(connection: Connection, character_name: str) -> Self:
        character_name = character_name.lower()
        cur = connection.cursor()
        cur.execute(
            RewardSql.select_character_by_character_name,
            (character_name,)
        )

        result = cur.fetchone()
        cur.close()

        return Character(*result)

    @staticmethod
    def get_characters_by_character_names(connection: Connection, characters: list[str]) -> list[Self]:
        return [Character.get_character_by_character_name(connection, character) for character in characters]
