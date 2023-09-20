from unittest.mock import MagicMock

import pytest

from patent_fetcher.call_api import (
    APIRequester,
    Config,
    USPTODataFetcher,
    USPTODataProcessor,
)
from patent_fetcher.data_saver import JsonDataSaver


@pytest.fixture
def api_requester():
    config = Config().get_config()
    return APIRequester(config)


@pytest.fixture
def uspto_instance():
    return USPTODataFetcher("2023-01-01", "2023-01-31")


@pytest.fixture
def data_processor():
    data_saver = JsonDataSaver()
    return USPTODataProcessor(data_saver)


def test_fetch_data_success(mock_requests_get, api_requester):
    response_data = {"results": []}
    mock_requests_get.return_value.json.return_value = response_data
    mock_requests_get.return_value.raise_for_status.return_value = None
    result = api_requester.fetch_data("2023-01-01", "2023-01-31", 0, 100, "Y")
    assert result == response_data


def test_fetch_data_failure(mock_requests_get, api_requester):
    mock_requests_get.return_value.raise_for_status.side_effect = Exception("Error")
    with pytest.raises(Exception, match="Error"):
        api_requester.fetch_data("2023-01-01", "2023-01-31", 0, 100, "Y")


def test_fetch_patent_data(data_processor, json_data_saver, uspto_instance):
    uspto_instance.data_processor = data_processor
    uspto_instance.data_saver = json_data_saver

    page_data = {"results": []}
    uspto_instance._fetch_data_page = MagicMock(return_value=page_data)
    uspto_instance._extract_data_docs = MagicMock(return_value=[])

    result = uspto_instance.fetch_patent_data()
    assert result is None


def test_fetch_patent_data_failure(uspto_instance):
    uspto_instance._fetch_data_page = MagicMock(side_effect=Exception("Error"))
    with pytest.raises(Exception, match="Error"):
        uspto_instance.fetch_patent_data()
