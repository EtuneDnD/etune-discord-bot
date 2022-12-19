from sqlite3 import Connection

from main.db.db_config import commit_close
from main.logic.exceptions.CustomExceptions import PaydayAlreadyClaimedError, UserHasNoCharactersError
from main.logic.models.character import Character
from main.logic.models.money_per_level import MoneyPerLevel
from main.logic.models.payday import Payday
from main.logic.models.reward import Reward
from main.logic.usecases.claim_payday.character_reward_summary import CharacterRewardSummary
from main.logic.usecases.claim_payday.response import Response


class ClaimPaydayUseCase:
    def __init__(self, username, author):
        self.username = username
        self.author = author

    def execute(self, con) -> Response:
        characters = Character.get_characters_by_username(con, self.username)

        if len(characters) > 0:
            if Payday.check_claimer_exists(con, self.username):
                if Payday.check_claimed(con, self.username):
                    con.close()
                    raise PaydayAlreadyClaimedError()

                else:
                    return self._claim_and_add_reward(con, self.username, characters, self.author)

            else:
                return self._add_new_claimer_and_add_reward(con, self.username, characters, self.author)

        else:
            con.close()
            raise UserHasNoCharactersError()

    @staticmethod
    def _claim_and_add_reward(con, username, characters, author):
        Payday.set_claimed(con, username)
        character_reward_list = ClaimPaydayUseCase._add_reward_per_level_to_characters(con, characters, author)
        commit_close(con)

        return Response("payday_claimed_succesfully", character_reward_list)

    @staticmethod
    def _add_new_claimer_and_add_reward(con, username, characters, author):
        Payday(username, True, author).insert_new_claimer(con)
        character_reward_list = ClaimPaydayUseCase._add_reward_per_level_to_characters(con, characters, author)
        commit_close(con)
        return Response("new_claimer_inserted", character_reward_list)

    @staticmethod
    def _add_reward_per_level_to_characters(
            con: Connection,
            characters: list[Character],
            author) -> list[CharacterRewardSummary]:
        character_reward_list = []
        for character in characters:
            money = ClaimPaydayUseCase._get_money_for_level(con, character)
            Reward(character.name, 0, money, False, author).insert_reward(con)
            character_reward_list.append(CharacterRewardSummary(character.name, character.level, money))
        return character_reward_list

    @staticmethod
    def _get_money_for_level(con, character) -> int:
        return MoneyPerLevel.select_all(con).dictionary.get(character.level, 0)
