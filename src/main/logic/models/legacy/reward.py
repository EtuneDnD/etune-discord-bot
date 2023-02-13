from sqlite3 import Connection
from typing import List, Self

from main.db.sql_statements import Reward as RewardSql


class Reward:
    def __init__(self, character_name: str, money: int, applied: bool, author: str,
                 acps: int = None, tcps: int = None, insertion_time: float = None, reward_id=None):
        self.tcps = tcps
        self.acps = acps
        self.insertion_time = insertion_time
        self.id = reward_id
        self.author = author
        self.applied = applied
        self.money = money
        self.character_name = character_name

    @staticmethod
    def get_and_consume_rewards(con: Connection, character_name: str) -> List[Self]:
        cur = con.cursor()

        rewards = Reward.get_rewards(con, character_name)
        Reward.consume_all_rewards(con, character_name)

        cur.close()

        return rewards

    @staticmethod
    def get_rewards(con: Connection, character_name: str) -> list[Self]:
        cur = con.cursor()
        cur.execute(
            RewardSql.select_rewads,
            (character_name,)
        )

        rewards = cur.fetchall()
        cur.close()

        return [Reward(*reward) for reward in rewards]

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

        rewards = cur.fetchone()[0]
        cur.close()

        return False if rewards == 0 else True

    def insert_reward(self, con: Connection):
        cur = con.cursor()

        cur.execute(
            RewardSql.insert_reward,
            (self.character_name, self.money, self.applied, self.author, self.acps, self.tcps)
        )

        cur.close()
