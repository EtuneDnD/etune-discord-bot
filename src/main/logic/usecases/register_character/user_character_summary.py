from main.logic.schemas.character_schema import Character
from main.logic.schemas.user_schema import User


class UserCharacterSummary:
    def __init__(self, user: User, character: Character):
        self.user = user
        self.character = character
