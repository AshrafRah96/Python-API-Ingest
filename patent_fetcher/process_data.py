import json
from abc import ABC, abstractmethod

from patent_fetcher.logs import Logger


class IDataSaver(ABC):
    """A data saver interface defining the contract for data saving strategies."""

    @abstractmethod
    def save(self, data: dict, output_config: dict) -> None:
        pass


class JsonDataSaver(IDataSaver):
    """A concrete data saver implementing JSON data saving strategy."""

    def save(self, data: dict, output_config: dict) -> None:
        with open(
            f'{output_config["directory"]}/output.{output_config["format"]}', "w"
        ) as f:
            json.dump(data, f, indent=4)


class DataProcessor:
    """A class coordinating the extraction and saving of data."""

    def __init__(self, config: dict, data_saver: IDataSaver) -> None:
        self.output_config = config["output"]
        self.data_saver = data_saver
        self.logging = Logger(config)

    def process_and_save_data(self, data: dict) -> None:
        if data:
            extracted_data = [
                DataExtractor.extract(item) for item in data["response"]["docs"]
            ]
            self.data_saver.save(extracted_data, self.output_config)
            self.logging.log_info(f"Data saved successfully, data saved: {len(data)}")
        else:
            self.logging.log_error("No data to save")


class DataExtractor:
    """A class responsible for extracting significant fields from data items."""

    @staticmethod
    def extract(data_item: dict) -> dict:
        return {
            "patentNumber": data_item.get("patentNumber"),
            "patentApplicationNumber": data_item.get("patentApplicationNumber"),
            "assigneeEntityName": data_item.get("assigneeEntityName"),
            "filingDate": data_item.get("filingDate"),
            "grantDate": data_item.get("grantDate"),
            "inventionTitle": data_item.get("inventionTitle"),
        }
