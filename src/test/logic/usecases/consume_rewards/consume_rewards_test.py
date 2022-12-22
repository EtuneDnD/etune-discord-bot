import unittest

from main.logic.usecases.consume_rewards.consume_rewards import ConsumeRewardsUseCase
from test.db.db_config_test import drop_tables, prepare_tables, connect


class TestConsumeRewardsUseCase(unittest.TestCase):
    def test_rewards_are_consumed(self):
        drop_tables()
        prepare_tables()

        con = connect()
        con.execute("INSERT INTO rewards (character_name, money, applied, author, acps, tcps) "
                    "VALUES ('test_character', 10, 0, 'test_author', 100, 120)")
        con.execute("INSERT INTO rewards (character_name, money, applied, author, acps, tcps) "
                    "VALUES ('test_character', 1, 0, 'test_author', 10, 12)")
        con.commit()
        con.close()

        response = ConsumeRewardsUseCase("test_character").execute(connect())

        con = connect()
        cur = con.cursor()
        result = cur.execute("SELECT * FROM rewards WHERE character_name = 'test_character'").fetchall()
        cur.close()
        con.close()

        for row in result:
            assert row[2] == 1
        assert response.status == "rewards_consumed"
        assert response.rewards_accumulated_summary.acp_acc == 110
        assert response.rewards_accumulated_summary.tcp_acc == 132
        assert response.rewards_accumulated_summary.money_acc == 11

    def test_no_rewards(self):
        drop_tables()
        prepare_tables()

        response = ConsumeRewardsUseCase("test_character").execute(connect())

        assert response.status == "no_rewards"
        assert response.rewards_accumulated_summary is None
