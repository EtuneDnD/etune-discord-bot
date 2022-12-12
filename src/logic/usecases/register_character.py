from db import db_config
from logic.character import Character
from logic.user import User


def assign_user_with_character(username: str, user_id: str, character_name: str, level: int, author: str):
    msg = ""
    con = db_config.connect()
    cur = con.cursor()

    if User.check_exists(cur, username):
        if Character.check_character_exists(cur, character_name):
            msg = "character_already_exists"
        else:
            Character(character_name, level, username, author).insert_character(cur)
            msg = "added_new_character"
    else:
        User(username, user_id, author).insert(cur)
        Character(character_name, level, username, author).insert_character(cur)
        msg = "inserted_new_user"

    con.commit()
    con.close()

    return msg
