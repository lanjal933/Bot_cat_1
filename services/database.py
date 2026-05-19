import sqlite3
import os

DB_PATH = "data/matchmaking.db"


def get_connection():

    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================
    # USERS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id TEXT PRIMARY KEY,

        role_player INTEGER DEFAULT 0,
        role_dm INTEGER DEFAULT 0,

        timezone TEXT
    )
    """)

    # =========================
    # AVAILABILITY
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS availability (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id TEXT,

        weekday TEXT,

        status TEXT,

        start_time TEXT,

        duration INTEGER
    )
    """)

    # =========================
    # QUEUE
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS matchmaking_queue (

        user_id TEXT PRIMARY KEY,

        joined_at TEXT,

        searching INTEGER DEFAULT 1
    )
    """)

    # =========================
    # GROUPS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups_table (

        group_id INTEGER PRIMARY KEY AUTOINCREMENT,

        dm_id TEXT,

        weekday TEXT,

        start_time TEXT,

        duration INTEGER,

        status TEXT
    )
    """)

    # =========================
    # GROUP MEMBERS
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS group_members (

        group_id INTEGER,

        user_id TEXT,

        confirmed INTEGER DEFAULT 0
    )
    """)

    conn.commit()

    conn.close()

    print("✅ Base de datos inicializada")

