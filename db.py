import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "database": "space_invaders_db",
    "user": "root",
    "password": ""
}


def get_connection():
    try:

        connection = mysql.connector.connect(
            **DB_CONFIG
        )

        if connection.is_connected():
            return connection

    except Error as e:

        print("MYSQL ERROR:", e)

    return None


def create_player(username, password):

    connection = get_connection()

    if connection is None:

        print("CREATE PLAYER: No database connection")

        return None

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO players
            (username, password)
            VALUES (%s, %s)
            """,
            (
                username,
                password
            )
        )

        connection.commit()

        print(
            "ACCOUNT CREATED:",
            username
        )

        return cursor.lastrowid

    except mysql.connector.IntegrityError as e:

        print(
            "USERNAME ALREADY EXISTS:",
            e
        )

        return None

    except Error as e:

        print(
            "CREATE PLAYER ERROR:",
            e
        )

        return None

    finally:

        cursor.close()
        connection.close()


def username_exists(username):

    connection = get_connection()

    if connection is None:

        print(
            "USERNAME CHECK: "
            "No database connection"
        )

        return False

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT player_id
            FROM players
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        return cursor.fetchone() is not None

    except Error as e:

        print(
            "USERNAME CHECK ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        connection.close()


def login_player(username, password):

    connection = get_connection()

    if connection is None:

        print(
            "LOGIN: "
            "No database connection"
        )

        return None

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                player_id,
                username,
                password
            FROM players
            WHERE username = %s
            LIMIT 1
            """,
            (username,)
        )

        player = cursor.fetchone()

        if player is None:

            print(
                "LOGIN: USER NOT FOUND"
            )

            return None

        if player["password"] != password:

            print(
                "LOGIN: WRONG PASSWORD"
            )

            return None

        print(
            "LOGIN SUCCESS:",
            username
        )

        return {
            "player_id":
                player["player_id"],

            "username":
                player["username"]
        }

    except Error as e:

        print(
            "LOGIN ERROR:",
            e
        )

        return None

    finally:

        cursor.close()
        connection.close()


def save_score(player_id, score):

    connection = get_connection()

    if connection is None:

        print(
            "SAVE SCORE: "
            "No database connection"
        )

        return False

    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO scores
            (player_id, score)
            VALUES (%s, %s)
            """,
            (
                player_id,
                score
            )
        )

        connection.commit()

        print(
            "SCORE SAVED:",
            score
        )

        return True

    except Error as e:

        print(
            "SAVE SCORE ERROR:",
            e
        )

        return False

    finally:

        cursor.close()
        connection.close()


def load_leaderboard():

    connection = get_connection()

    if connection is None:

        print(
            "LEADERBOARD: "
            "No database connection"
        )

        return []

    cursor = connection.cursor(
        dictionary=True
    )

    try:

        cursor.execute(
            """
            SELECT
                players.username,
                MAX(scores.score) AS score
            FROM scores
            INNER JOIN players
                ON players.player_id =
                   scores.player_id
            GROUP BY
                players.player_id,
                players.username
            ORDER BY
                score DESC,
                players.username ASC
            LIMIT 10
            """
        )

        results = cursor.fetchall()

        return results

    except Error as e:

        print(
            "LEADERBOARD ERROR:",
            e
        )

        return []

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":

    connection = get_connection()

    if connection:

        print(
            "MYSQL CONNECTION SUCCESS"
        )

        connection.close()

    else:

        print(
            "MYSQL CONNECTION FAILED"
        )