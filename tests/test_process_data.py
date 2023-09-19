import pytest
import logging
from patent_fetcher.process_data import (
    DataProcessor,
    IDataSaver, # Imported but not used
    JsonDataSaver,
    DataExtractor,
)
import json


class TestDataExtractor:
    def test_extract(self):
        data_item = {
            "patentNumber": "12345",
            "patentApplicationNumber": "67890",
            "assigneeEntityName": "Company ABC",
            "filingDate": "2023-01-01",
            "grantDate": "2023-02-01",
            "inventionTitle": "A Great Invention",
        }

        extracted_data = DataExtractor.extract(data_item)

        assert extracted_data == {
            "patentNumber": "12345",
            "patentApplicationNumber": "67890",
            "assigneeEntityName": "Company ABC",
            "filingDate": "2023-01-01",
            "grantDate": "2023-02-01",
            "inventionTitle": "A Great Invention",
        }


class TestJsonDataSaver:
    def test_save(self, tmp_path):
        data = [{"key": "value"}]
        output_config = {
            "directory": tmp_path,
            "format": "json",
            "output": {},
            "logging": {
                "level": "INFO",
                "logfile": "./patent_fetcher/logs/application.log",
            },
        }
        data_saver = JsonDataSaver()
        output_file = tmp_path / "output.json"

        data_saver.save(data, output_config)

        assert output_file.exists()
        with open(output_file, "r") as f:
            saved_data = json.load(f)
        assert saved_data == data


class TestDataProcessor:
    @pytest.fixture
    def data_processor(self, tmp_path):
        output_config = {
            "output": {"directory": tmp_path, "format": "json"},
            "logging": {
                "level": "INFO",
                "logfile": "./patent_fetcher/logs/application.log",
            },
        }
        data_saver = JsonDataSaver()
        return DataProcessor(output_config, data_saver)

    def test_process_and_save_data_with_data(self, data_processor, caplog):
        data = {
            "response": {
                "docs": [
                    {
                        "patentNumber": "12345",
                        "patentApplicationNumber": "67890",
                        "assigneeEntityName": "Company ABC",
                        "filingDate": "2023-01-01",
                        "grantDate": "2023-02-01",
                        "inventionTitle": "A Great Invention",
                    }
                ]
            }
        }

        with caplog.at_level(logging.INFO):
            data_processor.process_and_save_data(data)

        assert "Data saved successfully" in caplog.text

    def test_process_and_save_data_without_data(self, data_processor, caplog):
        data = None

        with caplog.at_level(logging.ERROR):
            data_processor.process_and_save_data(data)

        assert "No data to save" in caplog.text
