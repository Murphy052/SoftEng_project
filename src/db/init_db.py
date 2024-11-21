from src.db import get_db, get_db_cursor
from src.db.database import Database


def initialize_database(db: Database = get_db()):
    # SQL commands to create tables
    create_user_table = """
    CREATE TABLE IF NOT EXISTS "user" (
        id TEXT PRIMARY KEY,
        username TEXT,
        password TEXT
    );
    """

    create_inventory_table = """
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        name TEXT,
        rarity INTEGER,
        image TEXT,
        user_id INTEGER UNIQUE,
        FOREIGN KEY (user_id) REFERENCES "user"(id)
    );
    """

    create_items_table = """
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT,
        rarity INTEGER,
        image TEXT
    );
    """

    create_cases_table = """
    CREATE TABLE IF NOT EXISTS cases (
        id INTEGER PRIMARY KEY,
        name TEXT,
        image TEXT
    );
    """

    create_case_items_table = """
    CREATE TABLE IF NOT EXISTS case_items (
        case_id INTEGER,
        item_id INTEGER,
        PRIMARY KEY (case_id, item_id),
        FOREIGN KEY (case_id) REFERENCES cases(id),
        FOREIGN KEY (item_id) REFERENCES items(id)
    );
    """

    with get_db_cursor(db) as cursor:
        cursor.execute(create_user_table)
        cursor.execute(create_inventory_table)
        cursor.execute(create_items_table)
        cursor.execute(create_cases_table)
        cursor.execute(create_case_items_table)
