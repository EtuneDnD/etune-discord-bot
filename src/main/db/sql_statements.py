class Reward:
    # Selects
    select_exists_rewards = "SELECT COUNT(1) FROM rewards WHERE character_name = ? AND applied = 0;"
    select_rewads = "SELECT time_played, soul_stone, money FROM rewards WHERE character_name = ? AND applied = 0;"
    
    # Inserts
    insert_reward = "INSERT INTO rewards (character_name, time_played, money, applied, author, soul_stone) VALUES (?,?,?,?,?,?)"
    
    # Updates
    update_rewards_consumed = "UPDATE rewards SET applied = 1 WHERE character_name = ? AND applied = 0;"


class Payday:
    # Selects
    select_payday_check_exists = "SELECT COUNT(1) FROM payday WHERE username = ?;"
    select_payday_check_claimed = "SELECT COUNT(1) FROM payday WHERE username = ? AND claimed = 1;"

    # Inserts
    insert_new_claimer = "INSERT INTO payday (username, claimed, author) VALUES (?,?,?)"

    # Updates
    update_payday_claim = "UPDATE payday SET claimed = 1 WHERE username = ?"


class User:
    # Selects
    select_check_user_exists = "SELECT COUNT(1) FROM users WHERE username = ?"
    select_user = "SELECT * from users WHERE username = ?"
    
    # Inserts
    insert_user = "INSERT INTO users (username, user_id, author) VALUES (?,?,?)"


class Character:
    # Selects
    select_check_character_exists = "SELECT COUNT(1) FROM characters WHERE character_name = ?"
    select_user_characters = "SELECT * FROM characters WHERE username = ?"
    select_character_by_character_name = "SELECT * FROM characters WHERE character_name = ?"
    
    # Inserts
    insert_character = "INSERT INTO characters (character_name, level, username, author) VALUES (?,?,?,?)"

    # Updates
    update_character = "UPDATE characters (level, username, author, actor_base64) VALUES (?,?,?,?) WHERE character_name = ?"


class MoneyPerLevel:
    # Selects
    select_all = "SELECT level, copper_pieces FROM money_per_level"
    
    # Inserts
    insert_default_money_per_level = """
        INSERT INTO money_per_level (level, copper_pieces, author) VALUES
        (1, 150, 'Kaights#4231'),
        (2, 150, 'Kaights#4231'),
        (3, 150, 'Kaights#4231'),
        (4, 150, 'Kaights#4231'),
        (5, 300, 'Kaights#4231'),
        (6, 300, 'Kaights#4231'),
        (7, 300, 'Kaights#4231'),
        (8, 300, 'Kaights#4231'),
        (9, 300, 'Kaights#4231'),
        (10, 300, 'Kaights#4231'),
        (11, 450, 'Kaights#4231'),
        (12, 450, 'Kaights#4231'),
        (13, 450, 'Kaights#4231'),
        (14, 450, 'Kaights#4231'),
        (15, 450, 'Kaights#4231'),
        (16, 450, 'Kaights#4231'),
        (17, 600, 'Kaights#4231'),
        (18, 600, 'Kaights#4231'),
        (19, 600, 'Kaights#4231'),
        (20, 600, 'Kaights#4231')
        """


class Tables:
    all_tables = ["""
        CREATE TABLE IF NOT EXISTS rewards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_name VARCHAR(255),
            time_played INT NOT NULL,
            money INT NOT NULL,
            applied BOOLEAN NOT NULL,
            author VARCHAR(255) NOT NULL,
            soul_stone BOOLEAN NOT NULL,
            insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """, """
        CREATE TABLE IF NOT EXISTS payday (
            username VARCHAR(255) PRIMARY KEY,
            claimed BOOLEAN NOT NULL,
            author VARCHAR(255) NOT NULL,
            insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """, """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255) NOT NULL,
            author VARCHAR(255) NOT NULL,
            insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """, """
        CREATE TABLE IF NOT EXISTS characters (
            character_name VARCHAR(255) PRIMARY KEY,
            level INT NOT NULL,
            username VARCHAR(255),
            author VARCHAR(255) NOT NULL,
            insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            actor_base64 TEXT DEFAULT NULL,
            pushed BOOLEAN DEFAULT 0,
            FOREIGN KEY (username) REFERENCES user(username)
        )
    """, """
        CREATE TABLE IF NOT EXISTS money_per_level (
            level INT NOT NULL PRIMARY KEY,
            copper_pieces INT NOT NULL,
            author VARCHAR(255) NOT NULL,
            insertion_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
    """]
    