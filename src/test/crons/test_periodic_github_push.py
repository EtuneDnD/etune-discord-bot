import json
import unittest

import requests

from main.crons.periodic_github_push import periodic_github_push_action
from test.db.db_config_test import drop_tables, prepare_tables, connect


class TestPeriodicGithubPushCron(unittest.TestCase):
    def test_periodic_github_push_cron(self):
        drop_tables()
        prepare_tables()

        f = open("actor_test.json", "r")
        actor_json = json.load(f)
        actor_json = json.dumps(actor_json, indent=4)
        f.close()

        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.execute(f"INSERT INTO characters (character_name, level, username, author, actor_json) "
                    f"VALUES (?,?,?,?,?)", ("test_character", 3, "test_user", "test_author", actor_json))
        con.commit()
        con.close()

        periodic_github_push_action(connect())

        x = requests.get(
            "https://raw.githubusercontent.com/EtuneDnD/etune-shared-compendium-db/main/actors/test_character.json")

        con = connect()
        cur = con.cursor()
        result = cur.execute("SELECT pushed FROM characters WHERE character_name = ?", ("test_character",)).fetchone()

        assert x.text == actor_json
        assert result[0] == 1

    def test_periodic_github_push_with_several_actors(self):
        drop_tables()
        prepare_tables()

        f = open("actor_test.json", "r")
        actor_json = json.load(f)
        actor_json = json.dumps(actor_json, indent=4)
        f.close()

        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.execute(f"INSERT INTO characters (character_name, level, username, author, actor_json) "
                    f"VALUES (?,?,?,?,?)", ("test_character", 3, "test_user", "test_author", actor_json))
        con.execute(f"INSERT INTO characters (character_name, level, username, author, actor_json) "
                    f"VALUES (?,?,?,?,?)", ("test_character2", 3, "test_user", "test_author", actor_json))
        con.commit()
        con.close()

        periodic_github_push_action(connect())

        x = requests.get(
            "https://raw.githubusercontent.com/EtuneDnD/etune-shared-compendium-db/main/actors/test_character.json")
        y = requests.get(
            "https://raw.githubusercontent.com/EtuneDnD/etune-shared-compendium-db/main/actors/test_character2.json")

        con = connect()
        cur = con.cursor()
        result = cur.execute("SELECT pushed FROM characters WHERE character_name = ?", ("test_character",)).fetchone()
        result2 = cur.execute("SELECT pushed FROM characters WHERE character_name = ?", ("test_character2",)).fetchone()

        assert x.text == actor_json
        assert y.text == actor_json
        assert result[0] == 1
        assert result2[0] == 1
