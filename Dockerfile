# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container
COPY patent_fetcher/ /app/patent_fetcher/

# Define the command to run your CLI program with command-line arguments
ENTRYPOINT ["python", "-m", "patent_fetcher.cli"]
