import pytest

from patent_fetcher.process_data import DataExtractor, DataProcessor


def test_data_processor_initialization(data_saver):
    data_processor = DataProcessor(data_saver)
    assert data_processor.output_config is not None
    assert data_processor.data_saver == data_saver


def test_data_processor_process_and_save_data(data_processor):
    sample_data = [
        {
            "patentNumber": "12345",
            "patentApplicationNumber": "54321",
            "assigneeEntityName": "XYZ Corp",
            "filingDate": "2023-01-01",
            "grantDate": "2023-01-02",
            "inventionTitle": "Innovative Invention",
        }
    ]

    data_processor.process_and_save_data(sample_data)
    data_processor.data_saver.save.assert_called_once()


def test_data_extractor_extract():
    sample_item = {
        "patentNumber": "12345",
        "patentApplicationNumber": "54321",
        "assigneeEntityName": "XYZ Corp",
        "filingDate": "2023-01-01",
        "grantDate": "2023-01-02",
        "inventionTitle": "Innovative Invention",
    }

    expected_output = {
        "patentNumber": "12345",
        "patentApplicationNumber": "54321",
        "assigneeEntityName": "XYZ Corp",
        "filingDate": "2023-01-01",
        "grantDate": "2023-01-02",
        "inventionTitle": "Innovative Invention",
    }

    result = DataExtractor.extract(sample_item)
    assert result == expected_output
