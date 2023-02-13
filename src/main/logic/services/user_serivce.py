from sqlalchemy.orm import Session

from main.logic.models.user import User as UserModel
from main.logic.schemas.user_schema import UserCreate


def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()


def create_user(db: Session, user: UserCreate):
    db_user = UserModel(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()


def check_user_exists_by_id(db: Session, user_id: int) -> bool:
    exists = db.query(UserModel.id).filter_by(id=user_id).first() is not None

    return exists
