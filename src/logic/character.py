from sqlite3 import Cursor
from db.sql_statements import Character as character_sql_statements


def _check_character_exists(cur: Cursor, character_name: str):
  cur.execute(
    character_sql_statements.select_check_character_exists,
    (character_name,)
  )
  
  return False if cur.fetchone()[0] == 0 else True


def _insert_character(cur: Cursor, character_name: str, level: int, username: str, author: str):
  cur.execute(
    character_sql_statements.insert_character,
    (character_name, level, username, author)
  )


def _get_characters(cur: Cursor, username: str):
  cur.execute(
    character_sql_statements.select_user_characters,
    (username,)
  )
  
  result = cur.fetchall()
  
  return [
    {
      "character_name": tupla[0], 
      "level": tupla[1]
    } for tupla in result
  ]