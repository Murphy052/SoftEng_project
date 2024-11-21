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

        # Insert data into items table
        cursor.executemany("""
        INSERT INTO items (id, name, rarity, image) VALUES (?, ?, ?, ?)
        """, [
            (1, 'AK-47 | Bloodsport', 5, 'ak47_bloodsport.png'),
            (2, 'AWP | Oni Taiji', 4, 'awp_onitaiji.png'),
            (3, 'M4A4 | Hellfire', 3, 'm4a4_hellfire.png'),
            (4, 'USP-S | Neo-Noir', 3, 'usps_neonoir.png'),
            (5, 'AK-47 | Neon Revolution', 4, 'ak47_neonrevolution.png'),
            (6, 'SCAR-20 | Bloodsport', 2, 'scar20_bloodsport.png'),
            (7, 'Tec-9 | Fuel Injector', 3, 'tec9_fuelinjector.png'),
            (8, 'M4A1-S | Decimator', 4, 'm4a1s_decimator.png'),
            (9, 'AWP | Fever Dream', 5, 'awp_feverdream.png'),
            (10, 'M4A1-S | Chantico''s Fire', 5, 'm4a1s_chantico.png'),
        ])

        # Insert data into cases table
        cursor.executemany("""
        INSERT INTO cases (id, name, image) VALUES (?, ?, ?)
        """, [
            (1, 'Operation Hydra Case', 'operation_hydra_case.png'),
            (2, 'Spectrum Case', 'spectrum_case.png'),
            (3, 'Chroma 3 Case', 'chroma3_case.png'),
            (4, 'Gamma 2 Case', 'gamma2_case.png'),
        ])

        # Insert data into case_items table
        cursor.executemany("""
        INSERT INTO case_items (case_id, item_id) VALUES (?, ?)
        """, [
            (1, 2),  # Operation Hydra Case contains AWP | Oni Taiji
            (1, 3),  # Operation Hydra Case contains M4A4 | Hellfire
            (2, 1),  # Spectrum Case contains AK-47 | Bloodsport
            (2, 4),  # Spectrum Case contains USP-S | Neo-Noir
            (2, 8),  # Spectrum Case contains M4A1-S | Decimator
            (2, 9),  # Spectrum Case contains AWP | Fever Dream
            (3, 10),  # Chroma 3 Case contains M4A1-S | Chantico's Fire
            (4, 5),  # Gamma 2 Case contains AK-47 | Neon Revolution
            (4, 6),  # Gamma 2 Case contains SCAR-20 | Bloodsport
            (4, 7),  # Gamma 2 Case contains Tec-9 | Fuel Injector
        ])