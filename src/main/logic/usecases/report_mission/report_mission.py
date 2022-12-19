from sqlite3 import Connection

from main.db import db_config
from main.logic.models.character import Character
from main.logic.models.reward import Reward
from main.logic.models.user import User


class ReportMissionUseCase:
    def __init__(self, characters: list[str], time_played: int, money: int, author: str):
        self.characters = characters
        self.time_played = time_played
        self.money = money
        self.author = author

    def execute(self, con: Connection):
        Reward.add_rewards_to_characters(con, self.characters, self.time_played, self.money, self.author)
        character_user_list = self.get_character_user(con)

        db_config.commit_close(con)
        return character_user_list

    def get_character_user(self, con: Connection) -> list[dict[str, str]]:
        characters_obj = Character.get_characters_by_character_names(con, self.characters)
        character_user_list = []
        for character in characters_obj:
            setattr(character, "user", User.get(con, character.username))
            character_user_list.append(character)

        return character_user_list
