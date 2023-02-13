from main.db.db_config import commit_close
from main.logic.exceptions.CustomExceptions import CharacterAlreadyExistsError
from main.logic.models.legacy.character import Character
from main.logic.models.legacy.user import User
from main.logic.usecases.legacy.register_character.response import Response
from main.logic.usecases.legacy.register_character.user_character_summary import UserCharacterSummary


class RegisterCharacterUseCase:
    def __init__(self, username: str, user_id: str, character_name: str, level: int, author: str):
        self.username = username
        self.user_id = user_id
        self.character_name = character_name
        self.level = level
        self.author = author

    def execute(self, con):
        if User.check_exists(con, self.username):
            if Character.check_character_exists(con, self.character_name):
                con.close()
                raise CharacterAlreadyExistsError
            else:
                character = Character(self.character_name, self.level, self.username, self.author)
                character.insert_character(con)
                user = User.get(con, self.username)
                commit_close(con)
                return Response(
                    "added_new_character",
                    UserCharacterSummary(user, character)
                )
        else:
            user = User(self.username, self.user_id, self.author)
            user.insert(con)
            character = Character(self.character_name, self.level, self.username, self.author)
            character.insert_character(con)

            commit_close(con)
            return Response(
                "inserted_new_user",
                UserCharacterSummary(user, character)
            )
