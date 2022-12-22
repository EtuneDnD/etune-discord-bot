from pydantic import BaseModel


class ActorUpdateDTO(BaseModel):
    actor_json: str
    level: int
