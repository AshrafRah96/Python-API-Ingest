import json
import os

import pytest


def test_json_data_saver_save_new_file(json_data_saver, output_config):
    data = [{"key": "value1"}, {"key": "value2"}]
    json_data_saver.save(data, output_config)

    file_path = f'{output_config["directory"]}/output.{output_config["format"]}'
    with open(file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 2


def test_json_data_saver_save_existing_file(json_data_saver, output_config):
    initial_data = [{"key": "value1"}, {"key": "value2"}]
    json_data_saver.save(initial_data, output_config)

    data = [{"key": "value3"}]
    json_data_saver.save(data, output_config)

    file_path = f'{output_config["directory"]}/output.{output_config["format"]}'
    with open(file_path, "r") as f:
        lines = f.readlines()
        assert len(lines) == 3


def test_json_data_saver_save_data_integrity(json_data_saver, output_config):
    data = [{"key": "value1"}, {"key": "value2"}, {"key": "value3"}]
    json_data_saver.save(data, output_config)

    file_path = f'{output_config["directory"]}/output.{output_config["format"]}'
    with open(file_path, "r") as f:
        lines = f.readlines()
        saved_data = [json.loads(line.strip()) for line in lines]
        assert saved_data == data
