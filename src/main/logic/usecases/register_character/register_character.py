from main.db import db_config
from main.logic.models.character import Character
from main.logic.models.user import User


class RegisterCharacterUseCase:
    def __init__(self, username: str, user_id: str, character_name: str, level: int, author: str):
        self.username = username
        self.user_id = user_id
        self.character_name = character_name
        self.level = level
        self.author = author

    def execute(self):
        con = db_config.connect()
        cur = con.cursor()

        if User.check_exists(cur, self.username):
            if Character.check_character_exists(cur, self.character_name):
                raise CharacterAlreadyExistsError
            else:
                Character(self.character_name, self.level, self.username, self.author).insert_character(cur)
        else:
            User(self.username, self.user_id, self.author).insert(cur)
            Character(self.character_name, self.level, self.username, self.author).insert_character(cur)

        con.commit()
        con.close()
