from main.logic.usecases.legacy.consume_rewards.rewards_accumulated_summary import RewardsAccumulatedSummary


class Response:
    def __init__(self, status: str, rewards_accumulated_summary: RewardsAccumulatedSummary):
        self.status = status
        self.rewards_accumulated_summary = rewards_accumulated_summary
