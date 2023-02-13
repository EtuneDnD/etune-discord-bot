from main.logic.usecases.legacy.report_mission.character_user_reward import CharacterUserReward


class Response:
    def __init__(self, status: str, character_user_rewards: list[CharacterUserReward]):
        self.status = status
        self.character_user_rewards = character_user_rewards

