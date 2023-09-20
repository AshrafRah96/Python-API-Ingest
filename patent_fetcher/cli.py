"""This module initiates the process of fetching patent data from the USPTO API."""
import argparse

from patent_fetcher.call_api import USPTO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch patent data between two dates.")
    parser.add_argument("start_date", type=str, help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", type=str, help="End date in YYYY-MM-DD format")
    args = parser.parse_args()

    uspto_instance = USPTO(args.start_date, args.end_date)
    uspto_instance.fetch_patent_data()
