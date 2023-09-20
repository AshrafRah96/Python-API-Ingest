# USPTO Patent Fetcher Tech Test

## Description

This is a demo of using a CLI application that interacts with the USPTO's API to retrieve and store details of all patents conferred within a specified date range entered through CLI inputs.

The USPTO API documentation is accessible here for your reference:
USPTO API Documentation

Below is a sample API call using curl:

```
curl -X GET \
    --header 'Accept: application/json' \
    'https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate=2017-01-01&grantToDate=2017-01-03&start=0&rows=100&largeTextSearchFlag=N' \
    | gunzip > output.json
```

As a minimum i have saved these attributes as a json, but it is open for extension.

- patentNumber
- patentApplicationNumber
- assigneeEntityName
- filingDate
- grantDate
- inventionTitle

## Examples

The following invocation should save all patents granted between
April 25th 2001 and March 25th 2001 inclusive of both dates.

```bash
docker run patent_fetcher 2017-01-01 2017-01-03
```

note: you will need to run docker cp to extract output file from the container

## TLDR

The scripts call_api.py, data_saver.py, process_data.py, and cli.py effectively utilize design principles such as Single Responsibility Principle and Dependency Injection to create a scalable and maintainable software architecture. These principles foster modularity and flexibility, facilitating easy future expansions and adjustments. Moreover, robust error handling and logging mechanisms are in place, promoting swift issue identification and resolution, ensuring the application's reliability and stability. The approach thus lays a solid foundation for an adaptable, scalable, and reliable application ready for future developments.

### call_api.py

This script employs select design patterns and principles, enhancing its reliability and scalability. Below, we delve into these aspects:

Design Patterns and Principles

1. Single Responsibility Principle (SRP)
   Each class manages a distinct function: APIRequester handles API communications, USPTODataProcessor oversees data processing, and USPTODataFetcher coordinates the data retrieval and processing workflow. This modular approach encourages code reuse and simplifies upkeep.

2. Dependency Injection
   The USPTODataProcessor class accepts a data_saver instance, enabling various data saving strategies and facilitating component decoupling.

3. Composition Over Inheritance
   The USPTODataFetcher class integrates instances of APIRequester and USPTODataProcessor, endorsing the composition over inheritance principle, enhancing flexibility and function-specific encapsulation within separate classes.

4. Error Handling and Logging
   The script incorporates exception handling for potential API interaction errors, allowing graceful error management and efficient issue tracking through logging utilities.

Justification for this Approach:

Leveraging object-oriented principles, the script segregates tasks, making the code more manageable, testable, and adaptable. This setup, including the use of dependency injection, facilitates effortless integration of new data saving strategies in the future without altering the existing USPTODataProcessor class. Additionally, the extensive error handling and logging mechanisms guarantee application robustness, promoting quick issue identification and resolution, thus upholding the application's reliability.

In summary, this strategy provides a sturdy base for a scalable, maintainable application, paving the way for simple inclusion of new features or alterations later on.

## data_saver.py

The script embodies a thoughtful organization through the incorporation of fundamental design patterns and principles. Let's examine the key aspects:

Design Patterns and Principles

1. Single Responsibility Principle (SRP)
   The code structure adheres to the SRP, dividing tasks among distinct classes — DataProcessor for coordinating data saving and DataExtractor for data field extraction. This segregation fosters modularity and ease of maintenance.

2. Dependency Injection
   The DataProcessor class receives an IDataSaver instance during initialization, exhibiting dependency injection that facilitates a flexible and decoupled structure, thereby promoting adaptability with different data saving strategies.

3. Static Method
   DataExtractor employs a static method to extract data fields, eliminating the need for class instantiation and enhancing efficiency.

4. Logging and Error Handling
   The script employs robust logging and error handling mechanisms, aiding in efficient system monitoring and issue troubleshooting, hence enhancing the application's reliability.

Justification for this Approach:

This approach, characterized by modularity and flexibility, fosters code reusability and maintainability. The use of dependency injection adds to the system's adaptability, allowing for future extensions or modifications with minimal changes. Meanwhile, the static method in DataExtractor facilitates memory optimization.

Furthermore, the integrated logging and error handling mechanisms present a practical and robust framework for monitoring application performance and troubleshooting potential issues, establishing a reliable and stable application base. Overall, this design serves as a firm foundation for a scalable, maintainable, and adaptable application.

### process_data.py

Description and Principles:

The script employs several design principles enhancing its effectiveness:

Single Responsibility Principle (SRP): The DataProcessor and DataExtractor classes are each tasked with a specific function, promoting modular and reusable code.

Dependency Injection: DataProcessor accepts an IDataSaver instance, facilitating flexibility in choosing data saving strategies, which promotes component decoupling.

Encapsulation: Functions and data are bundled within respective classes, centralizing specific functionalities and making the code organized.

Error Handling and Logging: The script features robust error handling and logging utilities, aiding in effective debugging and ensuring application stability.

Justification for the Approach:

The script is structured to encourage scalability and maintainability. It adheres to SRP, fostering a modular design that simplifies future extensions. The utilization of Dependency Injection allows for adaptable data-saving strategies without altering existing classes, enhancing adaptability. Encapsulation helps in maintaining a focused and readable code base. Comprehensive error handling and logging ensure application robustness, facilitating quick issue resolution and reliability.

Overall, this approach sets a strong foundation for building an adaptable and sustainable application, ready to incorporate future features or modifications seamlessly.

### cli.py

This design allows for a clear separation of concerns, where the StartProcess class is responsible for coordinating the overall process, while the USPTO class handles API interaction and the DataProcessor class manages data processing and saving. Additionally, the script can be executed from the command line with start and end date arguments, making it a convenient and reusable tool for fetching patent data.
