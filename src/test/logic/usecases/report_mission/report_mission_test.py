import unittest

from main.logic.usecases.legacy.report_mission import ReportMissionUseCase
from test.db.db_config_test import drop_tables, prepare_tables, connect


class TestReportMissionUseCase(unittest.TestCase):
    def test_report_mission_returns_response_reward_created(self):
        drop_tables()
        prepare_tables()
        self.prepare_data()

        result = ReportMissionUseCase(["test_character_1", "test_character_2*", "test_character_3", "test_character_4"],
                                      122, "test_author").execute(connect())

        assert result.status == "rewards_added"
        assert next(x for x in result.character_user_rewards if x.character_name == "test_character_1").tcps == 122
        assert next(x for x in result.character_user_rewards if x.character_name == "test_character_1").acps == 122
        assert next(x for x in result.character_user_rewards if x.character_name == "test_character_2").acps == 122
        assert next(x for x in result.character_user_rewards if x.character_name == "test_character_2").tcps == 152

    def test_report_mission_returns_response_character_not_exists(self):
        drop_tables()
        prepare_tables()
        self.prepare_data()

        result = ReportMissionUseCase(
            ["test_character_fake", "test_character_2", "test_character_3", "test_character_4"],
            120, "test_author").execute(connect())

        assert result.status == "character_not_exists"

    def test_report_mission_returns_response_several_characters_from_same_player(self):
        drop_tables()
        prepare_tables()
        self.prepare_data()

        result = ReportMissionUseCase(
            ["test_character_1", "test_character_2", "test_character_4", "test_character_6"],
            120, "test_author").execute(connect())

        assert result.status == "characters_from_same_user"

    @staticmethod
    def prepare_data():
        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user_1', '123', 'test_author')")
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user_2', '234', 'test_author')")
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user_3', '345', 'test_author')")
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user_4', '456', 'test_author')")
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user_5', '456', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_1', 6, 'test_user_1', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_2', 11, 'test_user_2', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_3',15, 'test_user_3', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_4',20, 'test_user_4', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_5',20, 'test_user_5', 'test_author')")
        con.execute(
            "INSERT INTO characters (character_name, level, username, author) VALUES ('test_character_6',3, 'test_user_4', 'test_author')")
        con.commit()
        con.close()
