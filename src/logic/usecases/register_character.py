from logic import user
from logic import character
from db import db_config


def assign_user_with_character(username: str, character_name: str, level: int, author: str):
  msg = ""
  con = db_config.connect()
  cur = con.cursor()
  
  if user._check_user_exists(cur, username):
    if character._check_character_exists(cur, character_name):
      msg = "character_already_exists"
    else:
      character._insert_character(cur, character_name, level, username, author)
      msg = "added_new_character"
  else:
    user._insert_user(cur, username, author)
    character._insert_character(cur, character_name, level, username, author)
    msg = "inserted_new_user"
      
  con.commit()
  con.close()
  
  return msg