from unittest.mock import Mock, patch

import pytest

from patent_fetcher.config.config_manger import Config
from patent_fetcher.data_saver import IDataSaver, JsonDataSaver
from patent_fetcher.process_data import DataProcessor


@pytest.fixture
def config():
    return Config().get_config()


@pytest.fixture
def data_processor(data_saver):
    return DataProcessor(data_saver)


@pytest.fixture
def data_saver():
    return Mock(spec=IDataSaver)


@pytest.fixture
def json_data_saver():
    return JsonDataSaver()


@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock:
        mock.return_value.json.return_value = {"key": "value"}
        yield mock


@pytest.fixture
def output_config(tmp_path):
    return {"directory": tmp_path, "format": "json"}
