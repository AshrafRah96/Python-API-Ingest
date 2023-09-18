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
