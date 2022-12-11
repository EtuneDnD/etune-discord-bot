from sqlite3 import Cursor
from db import db_config
from db.sql_statements import Reward as reward_sql_statements


def add_rewards(characters: list[str], time_played: int, money: int, author: str):
    con = db_config.connect()
    cur = con.cursor()
    
    for character in characters:
        _insert_reward(cur, character, time_played, money, author)

    con.commit()
    con.close()


def check_rewards(character_name: str):
  con = db_config.connect()
  cur = con.cursor()

  has_rewards = _check_character_has_rewards(cur, character_name)
  
  con.close()
  
  return has_rewards


def get_and_consume_rewards(character_name: str):
  con = db_config.connect()
  cur = con.cursor()
  
  rewards = _get_rewards(cur, character_name)
  _consume_all_rewards(cur, character_name)

  con.commit()
  con.close()
  
  return rewards


def _get_rewards(cur: Cursor, character_name):
  cur.execute(
    db_config.select_rewads,
    (character_name,)
  )
  
  return cur.fetchall()


def _consume_all_rewards(cur: Cursor, character_name):
  cur.execute(
    db_config.update_rewards_consumed,
    (character_name,)
  )


def _check_character_has_rewards(cur: Cursor, character_name):
  cur.execute(
    reward_sql_statements.select_exists_rewards,
    (character_name,)
  )
  
  return cur.fetchone()


def _insert_reward(cur: Cursor, character_name: str, time_played: int, money: int, author: str):
  soul_stone = True
  
  if "*" in character_name:
      soul_stone = False
      
  cur.execute(
      reward_sql_statements.insert_reward, 
      (character_name.replace("*", ""), time_played, money, False, author, soul_stone)
  )
