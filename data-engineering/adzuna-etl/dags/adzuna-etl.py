import pandas as pd
from pandas.core.indexes.base import Index
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time
import datetime
import requests
import sqlite3
import json
import venv

def transform_data(df: pd.DataFrame):
    """
    This function validates the data returned by Adzuna API.
    Validation is performed as part of transform phase of ETL process.
    """

    # Check if no job listing is downloaded
    if df.empty:
        print("No job listing downlaoded!!")
        return False
    
    # Primay key check
    if pd.Series(df['job_id']).is_unique:
        pass
    else:
        raise Exception("Primary key is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found!")

    # Check that all timestamps are within 24 hours
    yesterday = int((datetime.datetime.now() - datetime.timedelta(days=1)).timestamp())

    timestamps = df["created"].tolist()

    row_indices = []

    for row_index, timestamp in enumerate(timestamps):
        if timestamp > yesterday:
            row_indices.append(row_index)

    df = df.drop(row_indices, inplace=True)

    return df

def run_adzuna_etl():

    # Set the location for the database
    database_location = "sqlite:///my_job_listings.sqlite"

    # These credentials are given by Adzuna on registration.
    # API_ID from Adzuna
    API_ID = "175bf19a"

    # API_KEY from Adzuna
    API_KEY = "286415dae8f2696be92e6c9f8470319a"
    
    # Extract part of the ETL process

    # API_KEY is used for authentication and since it is passed as a query parameter, there is no need to include it in header.
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json"
    }

    # The lists that contain each of the values from the API response are defined
    job_ids = []
    company_names = []
    job_titles = []
    categories = []
    locations = []
    salaries = []
    created_at = []
    descriptions = []
    ad_urls = []

    # Create a dictionary with the relevant values
    job_dict = {
        "job_id" : job_ids,
        "company_name" : company_names,
        "job_title" : job_titles,
        "category" : categories,
        "location" : locations,
        "salary" : salaries,
        "ad_url" : ad_urls,
        "created" : created_at,
        "description" : descriptions
    }

    # Convert the above created dictionary to a dataframe
    jobs_df = pd.DataFrame(
        job_dict,
        columns = ["job_id", "company_name", "job_title", "category", "location", "salary", "ad_url", "created", "description"]
        )

    # The API handles one page at a time with maximum of 50 results per page. Inorder to get the data from different pages, we
    # have to loop through the pages and then concatenate the results. Here, this project limits the pages to loop through as 5.

    for i in range (1, 6):
        r = requests.get(
            "https://api.adzuna.com/v1/api/jobs/gb/search/{page}?app_id={api_id}&app_key={api_key}"
            .format(page = i, api_id=API_ID, api_key=API_KEY),
            params = {'max_days_old': 1, 'results_per_page': 100},
            headers = headers
            )

        data = r.json()

        # Extract only relevant fields from Adzuna API response
        for job in data["results"]:
            job_ids.append(job["id"])
            company_names.append(job["company"]["display_name"])
            job_titles.append(job["title"].split('-')[0])
            categories.append(job["category"]["tag"])
            locations.append(job["location"]["display_name"])
            salaries.append(round(job["salary_max"]))
            ad_urls.append(job["redirect_url"])
            descriptions.append(job["description"])

            # Convert the "created at" to a unix timestamp
            date_time_str = job["created"].replace("T", " ")[: -1]
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            created_at.append(int(date_time_obj.timestamp()) * 1000)


        jobs_df.sort_values(by = ['created'], inplace = True, ascending = False)

        jobs_df.reset_index(inplace = True, drop = True)
 
        # Transform part of the ETL process
        jobs_df = transform_data(jobs_df)
        print("Data valid, proceed to next page")

run_adzuna_etl()


"""
To Do:

1. Understand where you place the data dictionary - whether inside the for loop or before that
2. How to update the dictionary with the new values
3. Do we have to validate each page result before adding to database?- how to do the validation step?
"""