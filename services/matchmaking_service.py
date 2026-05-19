import sqlite3

from datetime import datetime

from services.database import get_connection


# =========================
# REGISTER USER
# =========================

def register_user(
    user_id: str,
    is_player: bool,
    is_dm: bool,
    timezone: str
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO users (

        user_id,
        role_player,
        role_dm,
        timezone

    )

    VALUES (?, ?, ?, ?)

    """, (

        user_id,
        int(is_player),
        int(is_dm),
        timezone

    ))

    conn.commit()

    conn.close()


# =========================
# JOIN QUEUE
# =========================

def join_queue(user_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    INSERT OR REPLACE INTO matchmaking_queue (

        user_id,
        joined_at,
        searching

    )

    VALUES (?, ?, 1)

    """, (

        user_id,
        datetime.utcnow().isoformat()

    ))

    conn.commit()

    conn.close()


# =========================
# LEAVE QUEUE
# =========================

def leave_queue(user_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    DELETE FROM matchmaking_queue

    WHERE user_id = ?

    """, (user_id,))

    conn.commit()

    conn.close()


# =========================
# GET QUEUE USERS
# =========================

def get_queue_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM matchmaking_queue

    WHERE searching = 1

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================
# IS IN QUEUE
# =========================

def is_in_queue(user_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM matchmaking_queue

    WHERE user_id = ?

    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    return row is not None


# =========================
# GET USER
# =========================

def get_user(user_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

    SELECT *

    FROM users

    WHERE user_id = ?

    """, (user_id,))

    row = cursor.fetchone()

    conn.close()

    return row

# =========================
# SAVE AVAILABILITY
# =========================

def save_availability(

    user_id,
    weekday,
    status,
    start_time,
    duration

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO availability (

            user_id,
            weekday,
            status,
            start_time,
            duration

        )

        VALUES (?, ?, ?, ?, ?)
        """,

        (

            str(user_id),

            weekday,
            status,

            start_time,
            duration
        )
    )

    conn.commit()

    conn.close()

DB_PATH = "data/matchmaking.db"


# =========================
# REGISTER USER
# =========================

def register_user(

    user_id,
    is_player,
    is_dm

):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT OR REPLACE INTO matchmaking_users (

            user_id,
            is_player,
            is_dm

        )

        VALUES (?, ?, ?)
        """,

        (

            str(user_id),
            int(is_player),
            int(is_dm)

        )
    )

    conn.commit()

    conn.close()

    from services.database import get_connection


# =========================
# REGISTER USER
# =========================

def register_user(

    user_id,
    is_player=False,
    is_dm=False,
    timezone="UTC"

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT OR REPLACE INTO users (

            user_id,
            role_player,
            role_dm,
            timezone

        )

        VALUES (?, ?, ?, ?)
        """,

        (

            str(user_id),

            int(is_player),
            int(is_dm),

            timezone

        )

    )

    conn.commit()

    conn.close()

# =========================
# SAVE AVAILABILITY
# =========================

def save_availability(

    user_id,
    weekday,
    status

):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT INTO availability (

            user_id,
            weekday,
            status

        )

        VALUES (?, ?, ?)
        """,

        (

            str(user_id),
            weekday,
            status

        )
    )

    conn.commit()

    conn.close()

from datetime import datetime


# =========================
# JOIN QUEUE
# =========================

def join_queue(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        INSERT OR REPLACE INTO matchmaking_queue (

            user_id,
            joined_at,
            searching

        )

        VALUES (?, ?, ?)
        """,

        (

            str(user_id),

            datetime.utcnow().isoformat(),

            1
        )
    )

    conn.commit()

    conn.close()


# =========================
# LEAVE QUEUE
# =========================

def leave_queue(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        DELETE FROM matchmaking_queue
        WHERE user_id = ?
        """,

        (str(user_id),)
    )

    conn.commit()

    conn.close()


# =========================
# IS IN QUEUE
# =========================

def is_in_queue(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT * FROM matchmaking_queue
        WHERE user_id = ?
        """,

        (str(user_id),)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None
# =========================
# GET QUEUE USERS
# =========================

def get_queue_users():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT * FROM matchmaking_queue
        WHERE searching = 1
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# =========================
# GET USER AVAILABILITY
# =========================

def get_user_availability(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT * FROM availability
        WHERE user_id = ?
        """,

        (str(user_id),)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# =========================
# GET USER ROLES
# =========================

def get_user_roles(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT role_player, role_dm
        FROM users
        WHERE user_id = ?
        timezone
        """,

        (str(user_id),)
    )

    result = cursor.fetchone()

    conn.close()

    return 



# =========================
# REMOVE MULTIPLE USERS
# =========================

def remove_users_from_queue(user_ids):

    conn = get_connection()

    cursor = conn.cursor()

    for user_id in user_ids:

        cursor.execute(

            """
            DELETE FROM matchmaking_queue
            WHERE user_id = ?
            """,

            (str(user_id),)
        )

    conn.commit()

    conn.close()

# =========================
# PARSE HOUR
# =========================

def parse_hour(hour_text):

    horas, minutos = hour_text.split(":")

    return int(horas) * 60 + int(minutos)

# =========================
# CHECK COMPATIBILITY
# =========================

def are_users_compatible(user1_availability, user2_availability):

    for dia1 in user1_availability:

        for dia2 in user2_availability:

            # mismo dia
            if dia1["weekday"] != dia2["weekday"]:

                continue

            # evitar dias malos
            if dia1["status"] == "avoid":

                continue

            if dia2["status"] == "avoid":

                continue

            # horas
            inicio1 = parse_hour(dia1["start_time"])
            inicio2 = parse_hour(dia2["start_time"])

            fin1 = inicio1 + (dia1["duration"] * 60)
            fin2 = inicio2 + (dia2["duration"] * 60)

            # overlap
            inicio_max = max(inicio1, inicio2)
            fin_min = min(fin1, fin2)

            overlap = fin_min - inicio_max

            # minimo 2 horas compartidas
            if overlap >= 120:

                return True

    return False
# =========================
# TIMEZONE DIFFERENCE
# =========================

def timezone_difference(tz1, tz2):

    try:

        tz1 = int(str(tz1).replace("+", ""))
        tz2 = int(str(tz2).replace("+", ""))

        return abs(tz1 - tz2)

    except:

        return 999
# =========================
# COMPATIBILITY SCORE
# =========================

def compatibility_score(user1, user2):

    score = 0

    availability_1 = get_user_availability(user1["user_id"])
    availability_2 = get_user_availability(user2["user_id"])

    # =========================
    # TIMEZONE SCORE
    # =========================

    tz_diff = timezone_difference(

        user1["timezone"],
        user2["timezone"]
    )

    score += max(0, 10 - tz_diff)

    # =========================
    # DAY/HOUR SCORE
    # =========================

    for dia1 in availability_1:

        for dia2 in availability_2:

            if dia1["weekday"] != dia2["weekday"]:

                continue

            if dia1["status"] == "avoid":

                continue

            if dia2["status"] == "avoid":

                continue

            inicio1 = parse_hour(dia1["start_time"])
            inicio2 = parse_hour(dia2["start_time"])

            fin1 = inicio1 + (dia1["duration"] * 60)
            fin2 = inicio2 + (dia2["duration"] * 60)

            overlap = min(fin1, fin2) - max(inicio1, inicio2)

            if overlap > 0:

                # cada hora compartida suma score
                score += overlap // 60

                # ideal + ideal
                if dia1["status"] == "ideal":

                    if dia2["status"] == "ideal":

                        score += 5

    return score