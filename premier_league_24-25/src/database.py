import sqlite3
import logging


class DatabaseManager:
    """OOP approach to handle Database Management."""

    def __init__(self, db_name="premier_league.db"):
        self.db_name = db_name
        self._create_tables()

    def _get_connection(self):
        return sqlite3.connect(self.db_name)

    def _create_tables(self):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                # Table for Authentication
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        password_hash TEXT NOT NULL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def execute_query(self, query, params=()):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Query execution failed: {e}")
            return None