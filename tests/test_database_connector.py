"""Tests for DatabaseConnector class."""
import pytest
from unittest.mock import patch, MagicMock
from logic.classes.DatabaseConnector import DatabaseConnector, Singleton


class TestSingleton:
    """Tests for Singleton metaclass."""

    def test_returns_same_instance(self):
        # Reset singleton instances for this test
        Singleton._instances = {}

        instance1 = DatabaseConnector()
        instance2 = DatabaseConnector()

        assert instance1 is instance2

    def test_singleton_shares_state(self):
        Singleton._instances = {}

        instance1 = DatabaseConnector()
        instance1.is_connected = True

        instance2 = DatabaseConnector()
        assert instance2.is_connected is True


class TestDatabaseConnectorInit:
    """Tests for DatabaseConnector initialization."""

    @patch.dict('os.environ', {
        'DB_HOST': 'testhost',
        'DB_PORT': '5432',
        'DB_NAME': 'testdb',
        'DB_USER': 'testuser',
        'DB_PASSWORD': 'testpass'
    })
    def test_loads_config_from_env(self):
        Singleton._instances = {}

        connector = DatabaseConnector()

        assert connector.host == 'testhost'
        assert connector.port == 5432
        assert connector.database == 'testdb'
        assert connector.user == 'testuser'
        assert connector.password == 'testpass'

    def test_uses_defaults_when_env_missing(self):
        Singleton._instances = {}

        with patch.dict('os.environ', {}, clear=True):
            connector = DatabaseConnector()

            assert connector.host == 'localhost'
            assert connector.port == 3306
            assert connector.database == 'subot'
            assert connector.user == 'root'


class TestDatabaseConnectorConnect:
    """Tests for connect method."""

    @patch('logic.classes.DatabaseConnector.mysql.connector.connect')
    def test_connect_success(self, mock_connect):
        Singleton._instances = {}
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection

        connector = DatabaseConnector()
        connector.connect()

        assert connector.is_connected is True
        assert connector.con_obj is mock_connection

    @patch('logic.classes.DatabaseConnector.mysql.connector.connect')
    def test_connect_failure_raises_error(self, mock_connect):
        Singleton._instances = {}
        mock_connect.side_effect = Exception("Connection failed")

        connector = DatabaseConnector()

        with pytest.raises(ConnectionError):
            connector.connect()

        assert connector.is_connected is False


class TestDatabaseConnectorQueries:
    """Tests for query methods."""

    @patch('logic.classes.DatabaseConnector.mysql.connector.connect')
    def test_fetch_data_query_with_params(self, mock_connect):
        Singleton._instances = {}
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        connector = DatabaseConnector()
        connector.connect()

        result = connector.fetch_data_query(
            "SELECT * FROM table WHERE id = %s",
            (1,)
        )

        mock_cursor.execute.assert_called_once_with(
            "SELECT * FROM table WHERE id = %s",
            (1,)
        )
        assert result == [('row1',), ('row2',)]

    @patch('logic.classes.DatabaseConnector.mysql.connector.connect')
    def test_write_data_query_commits(self, mock_connect):
        Singleton._instances = {}
        mock_cursor = MagicMock()
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        connector = DatabaseConnector()
        connector.connect()

        connector.write_data_query(
            "INSERT INTO table (col) VALUES (%s)",
            ('value',)
        )

        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_fetch_raises_when_not_connected(self):
        Singleton._instances = {}
        connector = DatabaseConnector()

        with pytest.raises(ConnectionError):
            connector.fetch_data_query("SELECT 1")

    def test_write_raises_when_not_connected(self):
        Singleton._instances = {}
        connector = DatabaseConnector()

        with pytest.raises(ConnectionError):
            connector.write_data_query("INSERT INTO t VALUES (%s)", (1,))
