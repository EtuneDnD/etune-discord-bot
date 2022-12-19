import unittest

import pytest

from main.logic.exceptions.CustomExceptions import PaydayAlreadyClaimedError, UserHasNoCharactersError
from main.logic.models.payday import Payday
from main.logic.models.reward import Reward
from main.logic.usecases.claim_payday.character_reward_summary import CharacterRewardSummary
from main.logic.usecases.claim_payday.claim_payday import ClaimPaydayUseCase
from test.db.db_config_test import connect
from test.db.db_config_test import drop_tables
from test.db.db_config_test import prepare_tables


class TestClaimPaydayUseCase(unittest.TestCase):
    def test_claim_payday_returns_response_with_payday_claimed_succesfully(self):
        drop_tables()
        prepare_tables()
        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_1', 6, 'test_user', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_2',17, 'test_user', 'test_author')")
        con.execute("INSERT INTO payday (username, claimed, author) VALUES ('test_user', 0, 'test_user')")
        con.commit()
        con.close()

        result = ClaimPaydayUseCase("test_user", "test_author").execute(connect())

        con = connect()
        cur = con.cursor()
        reward_character_1 = Reward(
            *cur.execute("SELECT * FROM rewards WHERE character_name = 'test_character_1'").fetchone())
        reward_character_2 = Reward(
            *cur.execute("SELECT * FROM rewards WHERE character_name = 'test_character_2'").fetchone())
        payday = Payday(*cur.execute("SELECT * FROM payday WHERE username = 'test_user'").fetchone())
        cur.close()
        con.close()

        assert reward_character_1.money == 300
        assert not reward_character_1.applied
        assert reward_character_1.time_played == 0

        assert reward_character_2.money == 600
        assert not reward_character_2.applied
        assert reward_character_2.time_played == 0

        assert payday.claimed == 1
        assert result.status == "payday_claimed_succesfully"

        assert CharacterRewardSummary("test_character_1", 6, 300) in result.characters
        assert CharacterRewardSummary("test_character_2", 17, 600) in result.characters

    def test_claim_payday_returns_response_with_new_claimer_inserted(self):
        drop_tables()
        prepare_tables()

        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_1', 6, 'test_user', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_2',17, 'test_user', 'test_author')")
        con.commit()
        con.close()

        result = ClaimPaydayUseCase("test_user", "test_author").execute(connect())

        con = connect()
        cur = con.cursor()
        reward_character_1 = Reward(
            *cur.execute("SELECT * FROM rewards WHERE character_name = 'test_character_1'").fetchone())
        reward_character_2 = Reward(
            *cur.execute("SELECT * FROM rewards WHERE character_name = 'test_character_2'").fetchone())
        payday = Payday(*cur.execute("SELECT * FROM payday WHERE username = 'test_user'").fetchone())
        cur.close()
        con.close()

        assert reward_character_1.money == 300
        assert not reward_character_1.applied
        assert reward_character_1.time_played == 0

        assert reward_character_2.money == 600
        assert not reward_character_2.applied
        assert reward_character_2.time_played == 0

        assert payday.claimed == 1
        assert result.status == "new_claimer_inserted"

        assert CharacterRewardSummary("test_character_1", 6, 300) in result.characters
        assert CharacterRewardSummary("test_character_2", 17, 600) in result.characters

    def test_claim_payday_raises_payday_already_claimed(self):
        drop_tables()
        prepare_tables()
        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_1', 6, 'test_user', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_2',17, 'test_user', 'test_author')")
        con.execute("INSERT INTO payday (username, claimed, author) VALUES ('test_user', 1, 'test_user')")
        con.commit()
        con.close()

        with pytest.raises(PaydayAlreadyClaimedError):
            result = ClaimPaydayUseCase("test_user", "test_author").execute(connect())
            con = connect()
            cur = con.cursor()
            query = cur.execute("SELECT * FROM rewards").fetchall()
            cur.close()
            con.close()

            assert query == []
            assert result is None

    def test_claim_payday_raises_user_has_no_characters(self):
        drop_tables()
        prepare_tables()
        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.commit()
        con.close()

        with pytest.raises(UserHasNoCharactersError):
            result = ClaimPaydayUseCase("test_user", "test_author").execute(connect())

            con = connect()
            cur = con.cursor()
            rewards = cur.execute("SELECT * FROM rewards").fetchall()
            payday = cur.execute("SELECT * FROM payday").fetchall()
            cur.close()
            con.close()

            assert rewards == []
            assert payday == []
            assert result is None
