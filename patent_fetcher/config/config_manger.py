import pathlib
from os import path

import yaml


class Config:
    """A class to handle configuration settings.

    Attributes:
        config_file (str): The path to the configuration file.
        config (dict): A dictionary holding the configuration settings loaded from the config file.

    Methods:
        get_config(): Returns the configuration settings as a dictionary.
    """

    def __init__(self, config_file: str = "config.yaml") -> None:
        config_file = path.join(pathlib.Path(__file__).parent.resolve(), config_file)
        with open(config_file, "r") as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def get_config(self) -> dict:
        """Returns the configuration settings as a dictionary."""
        return self.config
