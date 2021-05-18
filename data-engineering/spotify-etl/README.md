## Introduction
This implements a data pipeline on Spotify's Recently Played tracks. The data is downloaded through Spotify API and is saved in SQLite database.

Spotify API token is generated from https://developer.spotify.com/console/get-recently-played/.

This pipeline is scheduled to run daily using Airflow.

## Setting Up the Project

 - Step 1: Get the access token from Spotify Developer Dashboard. For this, you need to have a user account on Spotify.
 - Step 2: Get the Spotify data using the above generated access token.
 - Step 3: Now, extract only relevant information from the json object and create a pandas dataframe.
 - Step 4: Validate the extracted data such as check whether data is downloaded, whether there are duplicates or whether there are null values, 
        etc. Also check whether all the timestamps are within 24 hours as we are interested in previous days's information only.
 - Step 5: Connect to any database. Here, I have chosen SQLite, a relational database and the ORM library used is sqlalchemy.
 - Step 6: Write the dataframe to the database.
 - Step 7: Inorder to automate this process, I have used Airflow. Set up Airflow in the machine or Docker. It is easy to follow the official 
        Airflow documentation.
 - Step 8: Once Airflow is configured, add dag file to your project directory.
 - Step 9: In your dag file, configure the airflow parameters and Operator.
 - Step 10: Now, start Airflow webserver and scheduler. Goto http://localhost:8080 in the browser and the dag should be listed there, if 
        everything worked well.
 - Step 11: We are ready to run the task. 

## Notes

 - Object Relational Matters (ORM) - Library that allows you to query SQL database from your coding environment. One such ORM is SQLAlchemy.

 - Directed Acyclic Graph (DAG) is a representation of series of events. Airflow DAG means that a collection of tasks that we need to run.  
   Each node in a DAG represents one task. 

## Credits
This is based on Karolina Sowinska's youtube video tutorial on data engineering.
 
(https://www.youtube.com/playlist?list=PLNkCniHtd0PNM4NZ5etgYMw4ojid0Aa6i)
