from main.logic.usecases.consume_rewards.rewards_accumulated_summary import RewardsAccumulatedSummary


class Response:
    def __init__(self, status: str, rewards_accumalated_summary: RewardsAccumulatedSummary):
        self.status = status
        self.rewards_accumalated_summary = rewards_accumalated_summary
