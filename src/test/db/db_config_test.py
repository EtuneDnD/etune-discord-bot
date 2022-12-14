import sqlite3

from main.db import sql_statements

db_url = "test_database.db"


def connect():
    return sqlite3.connect(db_url)


def prepare_tables():
    con = connect()
    cur = con.cursor()

    for create_table_statement in sql_statements.Tables.all_tables:
        cur.execute(create_table_statement)

    cur.execute(sql_statements.MoneyPerLevel.insert_default_money_per_level)

    con.commit()
    con.close()


def drop_tables():
    con = connect()

    tables = ['characters', 'money_per_level', 'payday', 'rewards', 'users']
    try:
        for table in tables:
            con.execute(f"DROP TABLE {table}")

        commit_close(con)
    except Exception:
        pass


def commit_close(con):
    con.commit()
    con.close()
