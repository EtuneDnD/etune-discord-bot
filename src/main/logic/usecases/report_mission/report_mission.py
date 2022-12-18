from sqlite3 import Cursor

from main.db import db_config
from main.logic.models.character import Character
from main.logic.models.reward import Reward
from main.logic.models.user import User


def report_mission(characters: list[str], time_played: int, money: int, author: str):
    con = db_config.connect()
    cur = con.cursor()
    Reward.add_rewards_to_characters(cur, characters, time_played, money, author)
    character_user_list = get_character_user(cur, characters)

    db_config.commit_close(con)
    return character_user_list


def get_character_user(cur: Cursor, characters: list[str]):
    characters_obj = Character.get_characters_by_character_names(cur, characters)
    character_user_list = []
    for character in characters_obj:
        setattr(character, "user", User.get(cur, character.username))
        character_user_list.append(character)

    return character_user_list
