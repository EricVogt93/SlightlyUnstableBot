"""Error handling for Discord command exceptions."""
import os
from typing import Dict, Optional

from logic.classes.ConfigHandler import ConfigHandler
from logic.helper.switchcase import SwitchCase


# Error type to handler mapping
ERROR_HANDLERS: Dict[str, str] = {
    "errors.CommandOnCooldown": "CommandOnCooldown",
    "errors.MissingPermissions": "MissingPermissions",
    "errors.MissingRequiredArgument": "MissingRequiredArgument",
    "errors.ConversionError": "ConversionError",
    "errors.CommandNotFound": "CommandNotFound"
}


class ErrorHandler:
    """Handles Discord command errors and returns appropriate messages."""

    def __init__(self, error: Exception) -> None:
        self.error_type = str(type(error))
        self.error_text = error.args[0] if error.args else str(error)

        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "ERRORS")
        self.error_messages = cfg.load()

    def get_error_message(self) -> str:
        """Get formatted error message for the error type."""
        switch = SwitchCase(ERROR_HANDLERS, self.error_type)
        handler_name = switch.match(partial=True)

        # Get the handler function
        handler = globals().get(handler_name, UnknownError)
        return handler(self.error_messages, self.error_text)

    # Backwards compatibility
    def check_error(self) -> str:
        return self.get_error_message()


def CommandOnCooldown(errors_config_settings, errortxt):
    txt = errors_config_settings["commandoncooldown"]
    return f"{txt} {errortxt})"


def MissingPermissions(errors_config_settings, errortxt):
    txt = errors_config_settings["missingpermissions"]
    return f"{txt} {errortxt})"


def MissingRequiredArgument(errors_config_settings, errortxt):
    txt = errors_config_settings["missingrequiredargument"]
    return f"{txt} {errortxt})"


def ConversionError(errors_config_settings, errortxt):
    txt = errors_config_settings["conversionerror"]
    return f"{txt} {errortxt})"


def CommandNotFound(errors_config_settings, errortxt):
    txt = errors_config_settings["commandnotfound"]
    return f"{txt} {errortxt})"


def UnknownError(errors_config_settings, errortxt):
    txt = errors_config_settings["unknownerror"]
    return f"{txt} {errortxt})"
