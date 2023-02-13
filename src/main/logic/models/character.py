from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from main.db.database import Base


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    level = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    character_json = Column(JSONB)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    owner = relationship("User", back_populates="characters")
    rewards = relationship("Reward", back_populates="rewarded_character")

