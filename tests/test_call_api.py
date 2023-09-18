from unittest.mock import Mock, patch

import pytest

from patent_fetcher.call_api import USPTO, APIRequester


# Mocking the APIRequester class
@pytest.fixture
def mock_api_requester():
    with patch("patent_fetcher.call_api.requests.get") as mock_get:
        yield mock_get


# Test data for APIRequester.fetch_data
fetch_data_test_data = [
    (
        "2023-01-01",
        "2023-01-31",
        0,
        10,
        "flag1",
        {
            "api": {
                "endpoint": "https://example.com/api",
                "row_limit": 10,
                "large_text_search_flag": "flag1",
                "start_index": 0,
                "rows_per_request": 10,
            }
        },
        {
            "grantFromDate": "2023-01-01",
            "grantToDate": "2023-01-31",
            "start": 0,
            "rows": 10,
            "largeTextSearchFlag": "flag1",
        },
        {"response": {"docs": [{"data": "document1"}]}},
    ),
    # Add more test cases as needed
]


@pytest.mark.parametrize(
    "start_date, end_date, start_index, row_limit, large_text_search_flag, api_config, expected_params, expected_response",
    fetch_data_test_data,
)
def test_api_requester_fetch_data(
    mock_api_requester,
    start_date,
    end_date,
    start_index,
    row_limit,
    large_text_search_flag,
    api_config,
    expected_params,
    expected_response,
):
    """Test APIRequester.fetch_data method."""
    api_requester = APIRequester(api_config=api_config)
    mock_api_requester.return_value.status_code = 200
    mock_api_requester.return_value.json.return_value = expected_response

    result = api_requester.fetch_data(
        start_date, end_date, start_index, row_limit, large_text_search_flag
    )

    mock_api_requester.assert_called_once_with(
        api_config["api"]["endpoint"],
        params=expected_params,
        headers={"Accept": "application/json"},
        verify=False,
    )
    assert result == expected_response


# Test data for USPTO._has_more_data
has_more_data_test_data = [
    ([{"data": "doc1"}, {"data": "doc2"}, {"data": "doc2"}], 0, 2, True),
    ([{"data": "doc1"}], 1, 10, False),
    ([], 0, 10, False),
]


@pytest.mark.parametrize(
    "data_docs, start_index, rows_per_request, expected_result", has_more_data_test_data
)
def test_uspto_has_more_data(data_docs, start_index, rows_per_request, expected_result):
    """Test USPTO._has_more_data method."""
    api_config = {
        "api": {
            "row_limit": 10,
            "large_text_search_flag": "flag1",
            "start_index": start_index,
            "rows_per_request": rows_per_request,
        },
        "logging": {"level": "INFO", "logfile": "./logs/application.log"},
    }
    uspto = USPTO("2023-01-01", "2023-01-31", api_config)
    uspto.all_data = data_docs

    result = uspto._has_more_data(data_docs)

    assert result == expected_result


# Test the fetch_patent_data method with mock responses
def test_uspto_fetch_patent_data(mock_api_requester):
    """Test USPTO.fetch_patent_data method."""
    api_config = {
        "api": {
            "endpoint": "https://example.com/api",
            "row_limit": 10,
            "large_text_search_flag": "flag1",
            "start_index": 0,
            "rows_per_request": 10,
        },
        "logging": {"level": "INFO", "logfile": "./logs/application.log"},
    }
    uspto = USPTO("2023-01-01", "2023-01-31", api_config)

    mock_api_requester.return_value.status_code = 200
    mock_api_requester.return_value.json.side_effect = [
        {"results": [{"data1": "doc1", "data2": "doc2", "data3": "doc3"}]},
    ]

    result = uspto.fetch_patent_data()

    assert result == {
        "response": {"docs": [{"data1": "doc1", "data2": "doc2", "data3": "doc3"}]}
    }


# Test the _extract_data_docs method
def test_uspto_extract_data_docs():
    """Test USPTO._extract_data_docs method."""
    api_config = {
        "api": {
            "row_limit": 10,
            "large_text_search_flag": "flag1",
            "start_index": 0,
            "rows_per_request": 10,
        },
        "logging": {"level": "INFO", "logfile": "./logs/application.log"},
    }
    uspto = USPTO("2023-01-01", "2023-01-31", api_config)
    response_data = {"results": [{"data": "doc1"}, {"data": "doc2"}]}

    result = uspto._extract_data_docs(response_data)

    assert result == [{"data": "doc1"}, {"data": "doc2"}]


# Test the fetch_patent_data method when an API error occurs
def test_uspto_fetch_patent_data_api_error(mock_api_requester):
    """Test USPTO.fetch_patent_data method when an API error occurs."""
    api_config = {
        "api": {
            "endpoint": "https://example.com/api",
            "row_limit": 10,
            "large_text_search_flag": "flag1",
            "start_index": 0,
            "rows_per_request": 10,
        },
        "logging": {"level": "INFO", "logfile": "./logs/application.log"},
    }
    uspto = USPTO("2023-01-01", "2023-01-31", api_config)

    mock_api_requester.return_value.status_code = 500

    result = uspto.fetch_patent_data()

    assert result == {"response": {"docs": []}}


# Custom exception for JSON decode error
class JSONDecodeError(Exception):
    pass


# Test the fetch_patent_data method when a JSON decode error occurs
def test_uspto_fetch_patent_data_json_decode_error(mock_api_requester):
    """Test USPTO.fetch_patent_data method when a JSON decode error occurs."""
    api_config = {
        "api": {
            "endpoint": "https://example.com/api",
            "row_limit": 10,
            "large_text_search_flag": "flag1",
            "start_index": 0,
            "rows_per_request": 10,
        },
        "logging": {"level": "INFO", "logfile": "./logs/application.log"},
    }
    uspto = USPTO("2023-01-01", "2023-01-31", api_config)

    mock_api_requester.return_value.status_code = 200
    mock_api_requester.return_value.json.side_effect = JSONDecodeError(
        "JSON Decode Error"
    )

    with pytest.raises(JSONDecodeError):
        uspto.fetch_patent_data()
