"""Tests for ConfigHandler class."""
import pytest
import tempfile
import os
from logic.classes.ConfigHandler import ConfigHandler


@pytest.fixture
def temp_config_file():
    """Create a temporary config file for testing."""
    content = """[DEFAULT]
token = test_token
database = test_db

[URL]
main_url = https://example.com
api_url = https://api.example.com

[SETTINGS]
debug = true
timeout = 30
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
        f.write(content)
        temp_path = f.name

    yield temp_path

    # Cleanup
    os.unlink(temp_path)


class TestGetValue:
    """Tests for get_value method."""

    def test_gets_value_from_default_section(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "DEFAULT")
        assert handler.get_value("token") == "test_token"
        assert handler.get_value("database") == "test_db"

    def test_gets_value_from_custom_section(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "URL")
        assert handler.get_value("main_url") == "https://example.com"

    def test_raises_key_error_for_missing_key(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "DEFAULT")
        with pytest.raises(KeyError):
            handler.get_value("nonexistent_key")


class TestLoad:
    """Tests for load method."""

    def test_loads_all_values_from_section(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "URL")
        settings = handler.load()

        assert "main_url" in settings
        assert "api_url" in settings
        assert settings["main_url"] == "https://example.com"

    def test_returns_dictionary(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "SETTINGS")
        settings = handler.load()

        assert isinstance(settings, dict)


class TestWrite:
    """Tests for write method."""

    def test_writes_new_values(self, temp_config_file):
        handler = ConfigHandler(temp_config_file, "test.ini", "SETTINGS")
        handler.load()  # Load first to initialize config

        handler.write({"new_key": "new_value"})

        # Read back and verify
        new_handler = ConfigHandler(temp_config_file, "test.ini", "SETTINGS")
        assert new_handler.get_value("new_key") == "new_value"
