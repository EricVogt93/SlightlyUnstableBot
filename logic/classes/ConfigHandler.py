import configparser


class ConfigHandler:
    FILE_NAME = None
    path = None
    config = None
    settings = {}
    root = None

    def __init__(self, path: object, filename: object, root: object) -> object:
        self.path = path
        self.config = configparser.ConfigParser()
        self.FILE_NAME = filename
        self.root = root

    def getValue(self, value):
        if not self.checkPath():
            self.config.read(self.path)
        else:
            self.config.read(f"{self.path}/{self.FILE_NAME}")
        return self.config[self.root][value]

    def load(self):
        if not self.checkPath():
            self.config.read(self.path)
        else:
            self.config.read(f"{self.path}/{self.FILE_NAME}")

        for key in self.config[self.root]:
            self.settings[key] = self.config[self.root][key]
        return self.settings

    def write(self, dict):
        for key in dict:
            self.config[self.root][key] = dict[key]
        with open(self.path, "w") as configfile:
            self.config.write(configfile)

    def checkPath(self):
        if self.path.endswith('ini'):
            return False
        else:
            return True
