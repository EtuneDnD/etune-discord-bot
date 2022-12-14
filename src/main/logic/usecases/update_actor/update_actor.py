from main.db.db_config import connect, commit_close

from main.logic.models.character import Character
from main.server.dto.actor_update_dto import ActorUpdateDTO


class UpdateActor:
    def __init__(self, character_name: str, actor_update: ActorUpdateDTO):
        self.character_name = character_name
        self.actor_update = actor_update

    def execute(self, con):
        if Character.check_character_exists(con, self.character_name):
            character = Character.get_character_by_character_name(con, self.character_name)
            character.level = self.actor_update.level
            character.actor_json = self.actor_update.actor_json
            character.update(con)
            commit_close(con)
