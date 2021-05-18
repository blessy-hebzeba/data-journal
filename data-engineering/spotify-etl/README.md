## Credits
This is based on Karolina Sowinska's youtube video course on data engineering. 
(https://www.youtube.com/playlist?list=PLNkCniHtd0PNM4NZ5etgYMw4ojid0Aa6i)

## Introduction
This implements a data pipeline on Spotify's Recently Played tracks. The data is downloaded through Spotify API and is saved in SQLite database.

Spotify API token is generated from https://developer.spotify.com/console/get-recently-played/.

This pipeline is scheduled to run daily using Airflow.

## Notes:

Object Relational Matters (ORM) - Library that allows you to query SQL database from your coding environment. One such ORM is SQLAlchemy.