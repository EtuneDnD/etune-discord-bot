from main.logic.usecases.claim_payday.character_reward_summary import CharacterRewardSummary


class Response:
    def __init__(self, status: str, characters: list[CharacterRewardSummary]):
        self.status = status
        self.characters = characters
