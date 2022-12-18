from pydantic import BaseModel


class ActorUpdateDTO(BaseModel):
    actor_base64: str
    level: int

