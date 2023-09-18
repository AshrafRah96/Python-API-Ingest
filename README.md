# USPTO Patent Fetcher Tech Test

## Description

Your task is to create a CLI program that calls the USPTO's API and saves patent
data for all granted patents granted between two dates provided as CLI arguments.

You can find documentation for the USPTO API here:
https://developer.uspto.gov/api-catalog/bulk-search-and-download

This is an example API request as a curl request

```
curl -X GET \
    --header 'Accept: application/json' \
    'https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate=2017-01-01&grantToDate=2017-01-03&start=0&rows=100&largeTextSearchFlag=N' \
    | gunzip > output.json
```

What data you save from the API response and where/how you persist this data is up to
you, but as a minimum we would like you to save these attributes.

- patentNumber
- patentApplicationNumber
- assigneeEntityName
- filingDate
- grantDate
- inventionTitle

Your solution should have the following characteristics

- Should not be public. Instead, please create a private GitHub repository and share this repository with [jamesstonehill](https://github.com/jamesstonehill) when you are done.
- Should be in Python.
- Should have unit tests. We don't expect full test coverage, but would like to
  see how you approach testing so if you are short on time, then you can write
  tests for part of your program, but please leave notes about where you are
  missing test coverage so we know that this was a conscious choice and not an
  inadvertent omission.
- Should be executable as a Docker executable.
- Should include notes on your solution and design decisions. These can be in the form of either
  inline comments or a README.
- Should log the progress of the patent fetching process.

## Examples

The following invocation should save all patents granted between
April 25th 2001 and March 25th 2001 inclusive of both dates.

```bash
docker run patent_fetcher 2017-01-01 2017-01-03
```

note: you will need to run docker cp to extract output file from the container

call_api.py = is designed to interact with the USPTO API, retrieve patent data within a specified date range, handle pagination, and log any errors encountered during the process. It separates concerns by using different classes for API requests, data processing, and logging, making the code modular and maintainable.

The usage of configuration settings allows for flexibility in adapting the code to different API endpoints and logging configurations. Additionally, error handling is implemented to handle potential issues such as network errors or JSON decoding errors during API requests.

process_data.py = follows the principles of separation of concerns and modularity. The IDataSaver interface allows for flexibility in implementing different data-saving strategies, and the JsonDataSaver class provides a concrete implementation for saving data in JSON format. The DataProcessor class coordinates the overall data processing and saving flow, and the DataExtractor class isolates the data extraction logic.

The use of configuration settings (config) allows for easy customization of output paths and logging configurations. Error handling is implemented to log errors and provide feedback in case of issues during data processing and saving.

logs.py = this Logger class provides a straightforward way to configure and use logging within an application. It allows for the separation of log levels and log messages, making it easy to control which messages are logged and where they are logged (e.g., to a file). It also adds an extra layer of customization by allowing different log types (error, info, warning) to be handled differently, such as with different log levels or destinations.

cli.py = This design allows for a clear separation of concerns, where the StartProcess class is responsible for coordinating the overall process, while the USPTO class handles API interaction and the DataProcessor class manages data processing and saving. Additionally, the script can be executed from the command line with start and end date arguments, making it a convenient and reusable tool for fetching patent data.
