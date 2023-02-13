from fastapi import Depends
from sqlalchemy.orm import Session

from main.db.database import get_db
from main.logic.models.user import User
from main.logic.schemas.character_schema import CharacterCreate
from main.logic.services.character_service import create_user_character, check_character_exists_by_name, \
    get_character_by_name
from main.logic.services.user_serivce import get_user_by_id, check_user_exists_by_id
from main.logic.usecases.register_character.response import Response
from main.logic.usecases.register_character.user_character_summary import UserCharacterSummary


class RegisterCharacterUseCase:

    def __init__(self, character_create: CharacterCreate):
        self.character_create = character_create

    def execute(self, db: Session = Depends(get_db)) -> Response:

        if check_user_exists_by_id(db, self.character_create.owner_id) is False:
            return
            # raise UserNotFoundError(f"User with id {self.character_create.owner_id} not found")

        if check_character_exists_by_name(db, self.character_create.name) is True:
            return
            # raise CharacterAlreadyExistsError(f"Character with name {self.character_create.name} already exists")

        create_user_character(db, self.character_create)

        return Response(
            "added_new_character",
            UserCharacterSummary(
                user=User()
            )
        )

