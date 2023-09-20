import json
import logging
from typing import List, Union

import requests

from patent_fetcher.config.config_manger import Config
from patent_fetcher.data_saver import JsonDataSaver

config = Config().get_config()
logging.basicConfig(level=config["logging"]["level"])
logging.getLogger(config["logging"]["logfile"])


class APIRequester:
    """A class to handle API requests and responses."""

    def __init__(self, api_config: dict) -> None:
        self.api_config = api_config

    def fetch_data(
        self,
        start_date: str,
        end_date: str,
        start_index: int,
        row_limit: int,
        large_text_search_flag: str,
    ) -> Union[dict, None]:
        """Fetches data from the API based on the specified parameters.

        This method forms a request with the provided parameters and sends it to
        the API endpoint. It handles potential request and JSON decoding exceptions
        gracefully by logging the errors and returning a dictionary containing the
        error message.

        Args:
            start_date (str): The start date for the data fetching in 'YYYY-MM-DD' format.
            end_date (str): The end date for the data fetching in 'YYYY-MM-DD' format.
            start_index (int): The starting index for data fetching, used for pagination.
            row_limit (int): The maximum number of rows to fetch in one request.
            large_text_search_flag (str): A flag to indicate whether to perform a large text search.

        Returns:
            Union[dict, None]: A dictionary containing the API response data if the request
            is successful, or a dictionary with an error message if an exception occurs,
            or None if JSON decoding fails.

        Raises:
            requests.exceptions.RequestException: If an error occurs during the API request.
            json.JSONDecodeError: If an error occurs during the JSON decoding process.

        Examples:
            >>> api_requester = APIRequester(api_config)
            >>> api_requester.fetch_data("2023-01-01", "2023-01-31", 0, 100, "Y")
            { ... response data ... }
        """
        url = self.api_config["api"]["endpoint"]
        params = {
            "grantFromDate": start_date,
            "grantToDate": end_date,
            "start": start_index,
            "rows": row_limit,
            "largeTextSearchFlag": large_text_search_flag,
        }
        try:
            response = requests.get(
                url,
                params=params,
                headers={"Accept": "application/json"},
                timeout=30,
                verify=False,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {str(e)}")
            return {"error": f"Request error: {str(e)}"}
        except json.JSONDecodeError as e:
            logging.error(f"JSON Decode error: {str(e)}")
            return {"error": f"JSON Decode error: {str(e)}"}


class USPTODataProcessor:
    """A class to handle data processing tasks."""

    def __init__(self, data_saver):
        self.data_saver = data_saver

    def process_and_save_data(self, data: List[dict]) -> None:
        # Add data processing logic here
        self.data_saver.save(data)


class USPTODataFetcher:
    """A class representing the USPTO data fetching module."""

    def __init__(self, start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.config = Config().get_config()
        self.api_requester = APIRequester(self.config)
        self.row_limit = self.config["api"]["row_limit"]
        self.large_text_search_flag = self.config["api"]["large_text_search_flag"]
        self.start_index = self.config["api"]["start_index"]
        self.data_flush_threshold = self.config["api"]["flush_threshold"]
        self.all_data = []
        self.data_saver = JsonDataSaver()
        self.data_processor = USPTODataProcessor(self.data_saver)

    def fetch_patent_data(self) -> Union[dict, None]:
        """Fetches and processes patent data in a loop until all data is retrieved.

        This method orchestrates the data fetching process by initiating a loop
        to send API requests and accumulate the retrieved data until it has all been fetched.
        To prevent memory overload, data is saved to disk in batches, adhering to
        a specified data flush threshold.

        Returns:
            Union[dict, None]: A dictionary containing the fetched data if the process
            is successful, or None if an error occurred during the data fetching process.

        Raises:
            requests.exceptions.RequestException: If there is an error during the API request.
            json.JSONDecodeError: If an error occurs during the JSON decoding process.

        Examples:
            >>> uspto = USPTODataFetcher(start_date="2023-01-01", end_date="2023-01-31")
            >>> uspto.fetch_patent_data()
            { ... response data ... }

        """
        data_flush_counter = 0

        response_data = self._fetch_data_page()
        data_docs = self._extract_data_docs(response_data)
        self.all_data.extend(data_docs)

        while self.all_data:
            data_flush_counter += 1
            if data_flush_counter >= self.data_flush_threshold:
                self._flush_data_to_disk()
                data_flush_counter = 0

    def _fetch_data_page(self) -> Union[dict, None]:
        response_data = self.api_requester.fetch_data(
            self.start_date,
            self.end_date,
            self.start_index,
            self.row_limit,
            self.large_text_search_flag,
        )
        if "error" in response_data:
            logging.error(response_data["error"])
            return None

        return response_data

    def _extract_data_docs(self, response_data: dict) -> List[dict]:
        return response_data.get("results", [])

    def _flush_data_to_disk(self) -> None:
        batch_data = self.all_data[: self.data_flush_threshold]
        self.all_data = self.all_data[self.data_flush_threshold :]
        self.data_processor.process_and_save_data(batch_data)
