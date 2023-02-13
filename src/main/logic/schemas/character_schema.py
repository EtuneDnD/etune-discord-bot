from pydantic import BaseModel
from datetime import datetime

from main.logic.schemas.user_schema import User


class CharacterBase(BaseModel):
    pass


class CharacterCreate(CharacterBase):
    name: str
    level: int
    owner_id: int


class Character(CharacterBase):
    id: int
    name: str
    level: int
    owner: User
    character_json: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
