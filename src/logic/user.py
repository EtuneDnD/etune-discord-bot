from sqlite3 import Cursor
from db.sql_statements import User as user_sql_statements


def _insert_user(cur: Cursor, username: str, author: str):
  cur.execute(
    user_sql_statements.insert_user,
    (username, author)
  )


def _check_user_exists(cur: Cursor, usernaname: str):
  cur.execute(
    user_sql_statements.select_check_user_exists,
    (usernaname,)
  )
  
  return False if cur.fetchone()[0] == 0 else True

