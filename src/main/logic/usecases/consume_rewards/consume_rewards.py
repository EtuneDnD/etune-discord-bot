from sqlite3 import Connection

from main.db.db_config import commit_close
from main.logic.models.reward import Reward
from main.logic.usecases.consume_rewards.response import Response
from main.logic.usecases.consume_rewards.rewards_accumulated_summary import RewardsAccumulatedSummary


class ConsumeRewardsUseCase:
    def __init__(self, character_name: str):
        self.character_name = character_name

    def execute(self, con: Connection):
        if Reward.check_character_has_rewards(con, self.character_name):
            rewards = Reward.get_and_consume_rewards(con, self.character_name)
            commit_close(con)
            return Response("rewards_consumed", self.group_rewards(rewards))
        else:
            return Response("no_rewards", None)

    @staticmethod
    def group_rewards(rewards: list[Reward]):
        tcp_acc = 0
        acp_acc = 0
        money_acc = 0

        for reward in rewards:
            tcp_acc += reward.tcps
            acp_acc += reward.acps
            money_acc += reward.money

        return RewardsAccumulatedSummary(tcp_acc, acp_acc, money_acc)