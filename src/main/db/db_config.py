import os
import sqlite3

from main.db import sql_statements


def connect():
    return sqlite3.connect(os.getenv("ETUNE_DB_PATH"))


def prepare_tables():
    con = connect()
    cur = con.cursor()

    for create_table_statement in sql_statements.Tables.all_tables:
        cur.execute(create_table_statement)

    try:
        cur.execute(sql_statements.MoneyPerLevel.insert_default_money_per_level)
    except sqlite3.IntegrityError:
        pass

    con.commit()
    con.close()


def commit_close(con):
    con.commit()
    con.close()
