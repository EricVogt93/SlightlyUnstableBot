import configparser
from typing import Any, Dict


class ConfigHandler:
    """Handles reading and writing INI configuration files."""

    def __init__(self, path: str, filename: str, section: str) -> None:
        self.path = path
        self.filename = filename
        self.section = section
        self.config = configparser.ConfigParser()
        self.settings: Dict[str, str] = {}

    def get_value(self, key: str) -> str:
        """Get a single value from the config section."""
        self._read_config()
        return self.config[self.section][key]

    def load(self) -> Dict[str, str]:
        """Load all values from the config section."""
        self._read_config()
        for key in self.config[self.section]:
            self.settings[key] = self.config[self.section][key]
        return self.settings

    def write(self, data: Dict[str, str]) -> None:
        """Write values to the config section."""
        for key, value in data.items():
            self.config[self.section][key] = value
        with open(self.path, "w") as configfile:
            self.config.write(configfile)

    def _read_config(self) -> None:
        """Read the config file from the appropriate path."""
        if self.path.endswith('.ini'):
            self.config.read(self.path)
        else:
            self.config.read(f"{self.path}/{self.filename}")
