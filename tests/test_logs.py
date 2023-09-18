import logging

import pytest

from patent_fetcher.logs import Logger


@pytest.fixture
def config():
    return {"logging": {"level": "INFO", "logfile": "test_log.log"}}


@pytest.fixture
def error_logger_instance(config):
    return Logger(config)


def test_initialization(error_logger_instance):
    assert isinstance(error_logger_instance, Logger)


def test_log_error(error_logger_instance, caplog):
    caplog.set_level(logging.ERROR)
    error_message = "Test error message"

    error_logger_instance.log_error(error_message)

    assert len(caplog.records) == 1
    assert caplog.records[0].levelname == "ERROR"
    assert caplog.records[0].message == error_message
