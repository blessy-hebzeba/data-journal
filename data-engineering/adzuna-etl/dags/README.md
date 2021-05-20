## Introduction
This project aims to create a dataset of job listings in the UK.

Adzuna is a UK based company that provides ob, property and car services. Adzuna API is RESTful API that helps to fetch all the job related information. There are mainly two job-related services- one is the hostorical data about jobs and other is up-to-the-minute job listings. This project uses the ad listings service.

To use the API, one has to register with Adzuna. Once registered, API_ID and API_KEY could be obtained from the dashboard. These are the required parameters along with page count in the API request. API_ID remians constant for the user, but multiple API_KEY could be generated and if needed, any chosen API_KEY could also be deleted.

They also provide an interactive endpoint doumentation where you could play around with different endpoints.

The further details about Adzuna API could be found here: https://developer.adzuna.com/overview.

## Setting Up

- Step 1: Register with Adzuna to get API_ID and API_KEY.
- Step 2: Extract the data by calling the API using requests method and save it as a Pandas dataframe.
