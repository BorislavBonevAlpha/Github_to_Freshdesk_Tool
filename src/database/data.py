import sqlite3
from sqlite3 import Connection
import os

db_path = os.path.join(os.path.dirname(__file__), 'database.db')


def _get_connection() -> Connection:
    return sqlite3.connect(db_path)


def create_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            username TEXT
        )
    ''')
    conn.commit()
    conn.close()


def read_query(sql: str, sql_params=()):
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with _get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount > 0
