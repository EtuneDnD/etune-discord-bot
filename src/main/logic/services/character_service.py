from sqlalchemy.orm import Session

from main.logic.models.character import Character as CharacterModel
from main.logic.schemas.character_schema import CharacterCreate, Character


def create_user_character(db: Session, character: CharacterCreate):
    db_character = CharacterModel(**character.dict(), owner_id=character.owner_id)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)

    return Character(**db_character.dict())


def get_character_by_name(db: Session, character_name: str):
    character_db = db.query(CharacterModel).filter_by(name=character_name).first()

    return Character(**character_db.dict())


def get_character_by_id(db: Session, character_id: int):
    character_db = db.query(CharacterModel).filter_by(id=character_id).first()

    return Character(**character_db.dict())
