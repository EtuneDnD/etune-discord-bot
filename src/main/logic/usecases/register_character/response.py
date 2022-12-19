from main.logic.usecases.register_character.user_character_summary import UserCharacterSummary


class Response:
    def __init__(self, status: str, user_character: UserCharacterSummary):
        self.status = status
        self.user_character = user_character

