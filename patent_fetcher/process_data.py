import logging

from patent_fetcher.config.config_manger import Config
from patent_fetcher.data_saver import IDataSaver

config = Config().get_config()
logging.basicConfig(level=config["logging"]["level"])
logging.getLogger(config["logging"]["logfile"])


class DataProcessor:
    """A class coordinating the extraction and saving of data."""

    def __init__(self, data_saver: IDataSaver) -> None:
        self.output_config = Config().get_config()["output"]
        self.data_saver = data_saver

    def process_and_save_data(self, data: dict) -> None:
        try:
            if data:
                extracted_data = [DataExtractor.extract(item) for item in data]
                self.data_saver.save(extracted_data, self.output_config)
                logging.info(f"Data saved successfully, data saved: {len(data)}")
            else:
                logging.error("No data to save")
        except Exception as e:
            logging.error(f"Failed to flush data from memory: {e}")


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
