from typing import Self
from sqlite3 import Cursor
from db import db_config
from db.sql_statements import Reward as RewardSql


class Reward:
    def __init__(self, character_name: str, time_played: int, money: int, applied: bool, author: str,
                 soul_stone: bool = True, insertion_time: float = None, reward_id=None):
        self.insertion_time = insertion_time
        self.id = reward_id
        self.soul_stone = soul_stone
        self.author = author
        self.applied = applied
        self.money = money
        self.time_played = time_played
        self.character_name = character_name

    @staticmethod
    def add_rewards_to_characters(cur: Cursor, characters_names: list[str], time_played: int, money: int, author: str):
        for character_name in characters_names:
            Reward(character_name, time_played, 0, False, author).insert_reward(cur)

    @staticmethod
    def check_rewards(character_name: str):
        con = db_config.connect()
        cur = con.cursor()

        has_rewards = Reward.check_character_has_rewards(cur, character_name)

        con.close()

        return has_rewards

    @staticmethod
    def get_and_consume_rewards(character_name: str):
        con = db_config.connect()
        cur = con.cursor()

        rewards = Reward.get_rewards(cur, character_name)
        Reward.consume_all_rewards(cur, character_name)

        con.commit()
        con.close()

        return rewards

    @staticmethod
    def get_rewards(cur: Cursor, character_name):
        cur.execute(
            db_config.select_rewads,
            (character_name,)
        )

        return cur.fetchall()

    @staticmethod
    def consume_all_rewards(cur: Cursor, character_name):
        cur.execute(
            db_config.update_rewards_consumed,
            (character_name,)
        )

    @staticmethod
    def check_character_has_rewards(cur: Cursor, character_name):
        cur.execute(
            RewardSql.select_exists_rewards,
            (character_name,)
        )

        return cur.fetchone()

    def insert_reward(self, cur: Cursor):
        soul_stone = True

        if "*" in self.character_name:
            soul_stone = False

        cur.execute(
            RewardSql.insert_reward,
            (self.character_name.replace("*", ""), self.time_played, self.money, False, self.author, soul_stone)
        )
