import json
from typing import List, Union

import requests

from patent_fetcher.logs import Logger


class APIRequester:
    """A class to handle API requests and responses.

    Attributes:
        api_config (dict): A dictionary holding the API configuration settings.
    """

    def __init__(self, api_config: dict) -> None:
        """Initializes APIRequester with API configuration settings.

        Args:
            api_config (dict): API configuration settings dictionary.
        """
        self.api_config = api_config

    def fetch_data(
        self,
        start_date: str,
        end_date: str,
        start_index: int,
        row_limit: int,
        large_text_search_flag: str,
    ) -> Union[dict, None]:
        """Fetches data from the API based on the provided parameters.

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            start_index (int): Starting index for pagination.
            row_limit (int): Row limit per API call.
            large_text_search_flag (str): Flag for large text search.

        Returns:
            Union[dict, None]: A dictionary containing the response data or None if an error occurs.
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
                url, params=params, headers={"Accept": "application/json"}, verify=False
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Request error: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"JSON Decode error: {str(e)}"}

        return response.json()


class USPTO:
    """A class representing the USPTO data fetching and processing module.

    Attributes:
        start_date (str): The start date for the data fetching range (YYYY-MM-DD).
        end_date (str): The end date for the data fetching range (YYYY-MM-DD).
        config (dict): The configuration settings dictionary.
        data_processor (DataProcessor): An instance of the DataProcessor class for handling data extraction and saving.
    """

    def __init__(self, start_date: str, end_date: str, config_manager: dict) -> None:
        """Initializes USPTO with necessary objects and configurations.

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.
            config_manager (dict): configs.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.config = config_manager
        self.api_requester = APIRequester(self.config)
        self.error_logger = Logger(self.config)
        self.row_limit = self.config["api"]["row_limit"]
        self.large_text_search_flag = self.config["api"]["large_text_search_flag"]
        self.start_index = self.config["api"]["start_index"]
        self.rows_per_request = self.config["api"]["rows_per_request"]
        self.all_data = []

    def fetch_patent_data(self) -> Union[dict, None]:
        """Fetches patent data from the USPTO API within the specified date range.

        It handles pagination to retrieve all records and implements error handling mechanisms.

        Returns:
            Union[dict, None]: A dictionary containing fetched data documents or None if an error occurs.
        """
        while True:
            response_data = self._fetch_data_page()
            if response_data is None:
                return None

            data_docs = self._extract_data_docs(response_data)
            self.all_data.extend(data_docs)

            if not self._has_more_data(data_docs):
                return {"response": {"docs": self.all_data}}

    def _fetch_data_page(self) -> Union[dict, None]:
        response_data = self.api_requester.fetch_data(
            self.start_date,
            self.end_date,
            self.start_index,
            self.row_limit,
            self.large_text_search_flag,
        )
        if "error" in response_data:
            self.error_logger.log_error(response_data["error"])
            return None

        return response_data

    def _extract_data_docs(self, response_data: dict) -> List[dict]:
        """Extracts data documents from the response data.

        Args:
            response_data (dict): The response data from the API.

        Returns:
            List[dict]: A list of data documents.
        """
        return response_data.get("results", [])

    def _has_more_data(self, data_docs: List[dict]) -> bool:
        """Checks if there are more data to fetch from the API.

        Args:
            data_docs (List[dict]): A list of data documents.

        Returns:
            bool: True if there are more data to fetch, False otherwise.
        """
        if len(data_docs) <= self.rows_per_request:
            return False
        self.start_index += self.rows_per_request
        return True
