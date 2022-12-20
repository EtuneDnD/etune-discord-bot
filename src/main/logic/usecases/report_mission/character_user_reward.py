from main.logic.models.user import User


class CharacterUserReward:
    def __init__(self, character_name: str, acps: int, tcps: int, user: User):
        self.tcps = tcps
        self.acps = acps
        self.character_name = character_name
        self.user = user
