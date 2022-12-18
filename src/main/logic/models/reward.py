from sqlite3 import Connection
from typing import List

from main.db.sql_statements import Reward as RewardSql


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
    def add_rewards_to_characters(con: Connection, characters_names: List[str], time_played: int, money: int,
                                  author: str):
        for character_name in characters_names:
            Reward(character_name, time_played, money, False, author).insert_reward(con)

    @staticmethod
    def check_rewards(con: Connection, character_name: str) -> bool:
        return Reward.check_character_has_rewards(con, character_name)

    @staticmethod
    def get_and_consume_rewards(con: Connection, character_name: str) -> List[tuple]:
        cur = con.cursor()

        rewards = Reward.get_rewards(cur, character_name)
        Reward.consume_all_rewards(cur, character_name)

        cur.close()

        return rewards

    @staticmethod
    def get_rewards(con: Connection, character_name: str) -> List[tuple]:
        cur = con.cursor()
        cur.execute(
            RewardSql.select_rewads,
            (character_name,)
        )

        rewards = cur.fetchall()
        cur.close()

        return rewards

    @staticmethod
    def consume_all_rewards(con: Connection, character_name: str):
        cur = con.cursor()
        cur.execute(
            RewardSql.update_rewards_consumed,
            (character_name,)
        )
        cur.close()

    @staticmethod
    def check_character_has_rewards(con: Connection, character_name: str) -> bool:
        cur = con.cursor()

        cur.execute(
            RewardSql.select_exists_rewards,
            (character_name,)
        )

        rewards = cur.fetchone()
        cur.close()

        return rewards

    def insert_reward(self, con: Connection):
        cur = con.cursor()
        soul_stone = True

        if "*" in self.character_name:
            soul_stone = False

        cur.execute(
            RewardSql.insert_reward,
            (self.character_name.replace("*", ""), self.time_played, self.money, False, self.author, soul_stone)
        )

        cur.close()
