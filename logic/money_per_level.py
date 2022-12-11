from sqlite3 import Cursor
from db.sql_statements import MoneyPerLevel as money_per_level_sql_statements


def _select_all(cur: Cursor):
    cur.execute(money_per_level_sql_statements.select_all)
    return dict(cur.fetchall())
