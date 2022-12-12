from bot import merlin
from db import db_config

if __name__ == "__main__":
    db_config.prepare_tables()
    merlin.start_bot()
