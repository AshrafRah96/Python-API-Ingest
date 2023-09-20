import json
import os
from abc import ABC, abstractmethod


class IDataSaver(ABC):
    """A data saver interface defining the contract for data saving strategies."""

    @abstractmethod
    def save(self, data: dict, output_config: dict) -> None:
        pass


class OtherTypesOfDataSaver(IDataSaver):
    """This is only to demonstrate the class has the options for extension"""

    pass


class JsonDataSaver(IDataSaver):
    """A concrete data saver implementing JSON data saving strategy."""

    def save(self, data: dict, output_config: dict) -> None:
        file_path = f'{output_config["directory"]}/output.{output_config["format"]}'
        mode = "a" if os.path.exists(file_path) else "w"

        with open(file_path, mode) as f:
            for record in data:
                json.dump(record, f)
                f.write("\n")
