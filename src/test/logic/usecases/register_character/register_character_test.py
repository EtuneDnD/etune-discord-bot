import unittest

import pytest

from main.logic.exceptions.CustomExceptions import CharacterAlreadyExistsError
from main.logic.usecases.register_character.register_character import RegisterCharacterUseCase
from test.db.db_config_test import drop_tables, prepare_tables, connect


class TestRegisterCharacterUseCase(unittest.TestCase):
    def test_register_character_returns_response_with_added_new_character(self):
        drop_tables()
        prepare_tables()

        con = connect()
        con.execute("INSERT INTO users (username, user_id, author) VALUES ('test_user', '123', 'test_author')")
        con.commit()
        con.close()

        result = RegisterCharacterUseCase("test_user", "123", "test_character", 3, "test_author").execute(connect())

        assert result.status == "added_new_character"
        assert result.user_character.character.username == "test_user"
        assert result.user_character.character.level == 3
        assert result.user_character.user.user_id == "123"
        assert result.user_character.user.username == "test_user"

    def test_register_character_returns_response_with_inserted_new_user(self):
        drop_tables()
        prepare_tables()

        result = RegisterCharacterUseCase("test_user", "123", "test_character", 3, "test_author").execute(connect())

        assert result.status == "inserted_new_user"
        assert result.user_character.character.username == "test_user"
        assert result.user_character.character.level == 3
        assert result.user_character.user.user_id == "123"
        assert result.user_character.user.username == "test_user"

    def test_register_character_returns_response_with_character_already_exists(self):
        drop_tables()
        prepare_tables()

        with pytest.raises(CharacterAlreadyExistsError):
            RegisterCharacterUseCase("test_user", "123", "test_character", 3, "test_author").execute(connect())
            RegisterCharacterUseCase("test_user", "123", "Test_character", 3, "test_author").execute(connect())
