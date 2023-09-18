"""This module initiates the process of fetching patent data from the USPTO API."""
import argparse
import os

from patent_fetcher.call_api import USPTO
from patent_fetcher.config.config_manger import Config
from patent_fetcher.process_data import DataProcessor, JsonDataSaver


class StartProcess:
    """A class to initiate the process of fetching patent data from the USPTO API.

    Methods:
        start: Starts the process of fetching and processing patent data.
    """

    def start(self, start_date, end_date, config):
        """Starts the process of fetching and processing the patent data.

        It creates instances of USPTO and DataProcessor classes and initiates the data fetching and processing.

        Args:
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.
            config (object): The configuration object containing API and output settings.
        """
        uspto_instance = USPTO(start_date, end_date, config)
        data = uspto_instance.fetch_patent_data()
        data_saver = JsonDataSaver()
        data_processor = DataProcessor(config, data_saver)
        data_processor.process_and_save_data(data)


if __name__ == "__main__":
    config = Config().get_config()

    parser = argparse.ArgumentParser(description="Fetch patent data between two dates.")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    args = parser.parse_args()

    process = StartProcess()
    process.start(args.start_date, args.end_date, config)
