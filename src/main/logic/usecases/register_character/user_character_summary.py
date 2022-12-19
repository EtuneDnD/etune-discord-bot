from main.logic.models.character import Character
from main.logic.models.user import User


class UserCharacterSummary:
    def __init__(self, user: User, character: Character):
        self.user = user
        self.character = character
