import sqlite3

DB_PATH = "data/matchmaking.db"


# =========================
# INIT DATABASE
# =========================

def init_matchmaking_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        """
        CREATE TABLE IF NOT EXISTS matchmaking_users (

            user_id TEXT PRIMARY KEY,

            is_player INTEGER DEFAULT 0,
            is_dm INTEGER DEFAULT 0

        )
        """
    )

    conn.commit()

    conn.close()