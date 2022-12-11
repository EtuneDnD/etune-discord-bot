from logic import payday
from logic import reward
from logic import character
from logic import money_per_level
from db import db_config


def claim_payday(username, author):
  con = db_config.connect()
  cur = con.cursor()
  
  characters = character._get_characters(cur, username)
  
  if len(characters) > 0:
    if payday._check_claimer_exists(cur, username):
      if payday._check_claimed(cur, username):
        commit_close(con)
        return response("payday_already_claimed", characters)
      
      else:
        payday._set_claimed(cur, username, author)
        add_reward_per_level_to_characters(cur, characters, author)      
        commit_close(con)
        return response("payday_claimed_succesfully", characters)
      
    else:
      payday._insert_new_claimer(cur, username, author)
      add_reward_per_level_to_characters(cur, characters, author)
      commit_close(con)
      return response("new_claimer_inserted", characters)
    
  else:
    commit_close(con)
    return response("user_has_no_characters", characters)

def add_reward_per_level_to_characters(cur, characters, author):
  for character in characters:
    money = get_money_for_level(cur, character)
    reward._insert_reward(cur, character['character_name'], 0, money, author)
    character['money'] = money

def get_money_for_level(cur, character):
  money_per_level._select_all(cur).get(character['level'], 0)

def response(msg, characters):
  return {
      "status": msg,
      "characters": characters
    }

def commit_close(con):
  con.commit()
  con.close()