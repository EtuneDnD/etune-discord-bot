from sqlite3 import Cursor
from db.sql_statements import Payday as payday_sql_statements


def _set_claimed(cur: Cursor, username: str, author: str):
    cur.execute(
                payday_sql_statements.update_payday_claim,
                (username,)
    )


def _insert_new_claimer(cur: Cursor, username: str, author: str):
    cur.execute(
        payday_sql_statements.insert_new_claimer,
        (username, True, author)
    )      


def _check_claimer_exists(cur: Cursor, username: str):
    cur.execute(
        payday_sql_statements.select_payday_check_exists,
        (username,)
    )
    
    return False if cur.fetchone()[0]== 0 else True


def _check_claimed(cur: Cursor, username: str):
    cur.execute(
        payday_sql_statements.select_payday_check_claimed,
        (username,)
    )
    return True if cur.fetchone()[0] == 1 else False

