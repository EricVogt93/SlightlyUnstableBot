import logging
import os
from contextlib import contextmanager
from typing import Any, Generator, List, Optional, Tuple

import mysql.connector

from logic.helper.singleton import Singleton

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)


class DatabaseConnector(metaclass=Singleton):
    """
    Handles MySQL database connections and queries.

    Can be used as a context manager for automatic connection handling:
        with get_db() as db:
            result = db.fetch_data_query("SELECT * FROM table")
    """

    def __init__(self) -> None:
        self.con_obj: Optional[mysql.connector.MySQLConnection] = None
        self.is_connected: bool = False

        # Load database config from environment variables
        self.host: str = os.getenv("DB_HOST", "localhost")
        self.port: int = int(os.getenv("DB_PORT", "3306"))
        self.database: str = os.getenv("DB_NAME", "subot")
        self.user: str = os.getenv("DB_USER", "root")
        self.password: str = os.getenv("DB_PASSWORD", "")

    def connect(self) -> None:
        """Establish connection to the MySQL database."""
        try:
            self.con_obj = mysql.connector.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.is_connected = True
        except mysql.connector.Error as e:
            self.is_connected = False
            raise ConnectionError(f"Database connection failed: {e}")

    def close(self) -> None:
        """Close the database connection."""
        try:
            if self.con_obj:
                self.con_obj.close()
            self.is_connected = False
        except mysql.connector.Error as e:
            raise ConnectionError(f"Failed to close database connection: {e}")

    def write_data_query(self, sql: str, params: Optional[Tuple] = None) -> None:
        """Execute an INSERT/UPDATE/DELETE query with parameters."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        cursor = self.con_obj.cursor()
        try:
            cursor.execute(sql, params)
            self.con_obj.commit()
        except mysql.connector.Error as e:
            self.con_obj.rollback()
            raise RuntimeError(f"Query execution failed: {e}")
        finally:
            cursor.close()

    def fetch_data_query(self, sql: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """Execute a SELECT query with optional parameters and return results."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        cursor = self.con_obj.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            raise RuntimeError(f"Query execution failed: {e}\nQuery: {sql}")
        finally:
            cursor.close()


@contextmanager
def get_db() -> Generator[DatabaseConnector, None, None]:
    """
    Context manager for database operations.

    Automatically connects and closes the database connection.

    Usage:
        with get_db() as db:
            result = db.fetch_data_query("SELECT * FROM table")

    Yields:
        DatabaseConnector: Connected database instance
    """
    db = DatabaseConnector()
    db.connect()
    try:
        yield db
    finally:
        db.close()
