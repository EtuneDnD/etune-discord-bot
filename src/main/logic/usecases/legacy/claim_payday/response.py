from main.logic.usecases.legacy.claim_payday.character_reward_summary import CharacterRewardSummary


class Response:
    def __init__(self, status: str, characters_rewards: list[CharacterRewardSummary]):
        self.status = status
        self.characters_rewards = characters_rewards

