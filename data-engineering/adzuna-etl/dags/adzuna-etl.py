import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import datetime
import requests
import sqlite3
import json
import venv


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

    r = requests.get("https://api.adzuna.com/v1/api/jobs/gb/search/20?app_id={api_id}&app_key={api_key}".format(api_id=API_ID, api_key=API_KEY), headers = headers)

    data = r.json()

    company_names = []
    job_titles = []
    categories = []
    locations = []
    salaries = []
    created_at = []
    descriptions = []
    ad_urls = []

    # Extract only relevant fields from Adzuna API response
    for job in data["results"]:
        company_names.append(job["company"]["display_name"])
        job_titles.append(job["title"].split('-')[0])
        categories.append(job["category"]["tag"])
        locations.append(job["location"]["display_name"])
        salaries.append(round(job["salary_max"]))
        ad_urls.append(job["redirect_url"])
        created_at.append(job["created"])
        descriptions.append(job["description"])

    # Create a dictionary with the relevant values
    job_dict = {
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
    jobs_df = pd.DataFrame(job_dict, columns = ["company_name", "job_title", "category", "location", "salary", "ad_url", "created", "description"])

run_adzuna_etl()