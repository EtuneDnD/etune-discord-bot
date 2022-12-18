from main.logic.models.character import Character
from main.server.dto.ActorUpdateDTO import ActorUpdateDTO
from src.main.db.db_config import connect


class UpdateActor:

    def __init__(self, character_name: str, actor_update: ActorUpdateDTO):
        self.character_name = character_name
        self.actor_update = actor_update

    def execute(self, con=connect()):
        if Character.check_character_exists(con, self.character_name):
            character = Character.get_character_by_character_name(con, self.character_name)
            character.level = self.actor_update.level
            character.actor_base64 = self.actor_update.actor_base64
            character.update(con)
