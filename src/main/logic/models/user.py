from datetime import datetime

from sqlalchemy import Boolean, DateTime, Column, Integer, String
from sqlalchemy.orm import relationship

from main.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    characters = relationship("Character", back_populates="owner")
    rewards_applied = relationship("Reward", back_populates="author")
    paydays = relationship("Payday", back_populates="user")
