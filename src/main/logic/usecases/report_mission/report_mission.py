from sqlite3 import Connection

from main.db.db_config import commit_close
from main.logic.models.character import Character
from main.logic.models.reward import Reward
from main.logic.models.user import User
from main.logic.usecases.report_mission.character_user_reward import CharacterUserReward
from main.logic.usecases.report_mission.response import Response


class ReportMissionUseCase:
    def __init__(self, character_names: list[str], time_played: int, author: str):
        self.character_names = [element.lower() for element in character_names]
        self.character_names_clean = [character_name.replace("*", "") for character_name in self.character_names]
        self.time_played = time_played
        self.author = author

    def execute(self, con: Connection) -> Response:
        if Character.check_characters_exist(con, self.character_names_clean):
            characters = Character.get_characters_by_character_names(con, self.character_names_clean)
            if self.check_characters_from_different_users(characters):
                self.add_soulstone_to_characters(characters, self.character_names)
                character_user_reward_list = self.add_rewards_to_characters(
                    con,
                    characters,
                    self.time_played,
                    self.author
                )
                commit_close(con)
                return Response("rewards_added", character_user_reward_list)
            else:
                commit_close(con)
                return Response("characters_from_same_user", None)
        else:
            commit_close(con)
            return Response("character_not_exists", None)

    @staticmethod
    def add_soulstone_to_characters(characters: list[Character], character_names: list[str]):
        for character_name in character_names:
            for character in characters:
                if character.name == character_name.replace("*", ""):
                    if "*" in character_name:
                        setattr(character, "soul_stone", True)
                    else:
                        setattr(character, "soul_stone", False)

    @staticmethod
    def check_characters_from_different_users(characters) -> bool:
        usernames = [character.username for character in characters]
        if len(set(usernames)) == len(characters):
            return True
        else:
            return False

    def add_rewards_to_characters(self, con: Connection, characters: list[Character], time_played: int, author: str):
        character_user_reward_list = []
        for character in characters:
            reward = ""

            if character.soul_stone:
                character.name = character.name.replace("*", "")
                reward = Reward(
                    character_name=character.name,
                    money=0,
                    applied=False,
                    author=author,
                    acps=self.time_played,
                    tcps=round(time_played * 1.25)
                )
            else:
                reward = Reward(
                    character_name=character.name,
                    money=0,
                    applied=False,
                    author=author,
                    acps=self.time_played,
                    tcps=self.time_played
                )

            character_user_reward_list.append(
                CharacterUserReward(
                    character_name=character.name,
                    acps=reward.acps,
                    tcps=reward.tcps,
                    user=User.get(con, character.username)
                )
            )

        return character_user_reward_list
