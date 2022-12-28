import datetime
from sqlite3 import Connection

from dotenv import load_dotenv

from main.db.db_config import connect


def reset_paydays(con: Connection):
    cur = con.cursor()
    cur.execute("UPDATE payday SET claimed = 0")
    cur.close()


if __name__ == '__main__':
    load_dotenv(dotenv_path="..\\.env")
    reset_paydays(connect())
    print(f"[{datetime.datetime.now()}] - Reseting payday claims.")
