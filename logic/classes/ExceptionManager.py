import os

from Handler.ConfigHandler import ConfigHandler
from Helper.switchcase import switchcase


class ErrorHandler:
    error = None
    obj = None
    error_dictionary = None
    errors_config_settings = None

    def __init__(self, error):
        self.error = str(type(error))
        self.errortxt = error.args[0]
        self.buildDict()

        cfg = ConfigHandler(os.path.join("res", "bot_config.ini"), "bot_config.ini", "ERRORS")
        self.errors_config_settings = cfg.load()

    def checkError(self):
        switch = switchcase(self.error_dictionary, self.error)
        errorhandling = switch.compare(True)
        # dynamischer function call
        method = globals()[errorhandling]
        return method(self.errors_config_settings, self.errortxt)

    def buildDict(self):
        self.error_dictionary = {
            "errors.CommandOnCooldown": "CommandOnCooldown",
            "errors.MissingPermissions": "MissingPermissions",
            "errors.MissingRequiredArgument": "MissingRequiredArgument",
            "errors.ConversionError": "ConversionError",
            "errors.CommandNotFound": "CommandNotFound"
        }


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
