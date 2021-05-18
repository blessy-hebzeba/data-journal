import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"

# Username of Spotify account
USER_ID = "0ae40oyrgzs03en0wp946cz6b"

# Token ID from Spotify API
TOKEN = "BQBfhwuUdpWikHhe3yuhWFXWgsLKcbbLkCEaVDOP0VtIf7vh3RspD-iQ8R23DmHUh260nCodhsLD4XD1HWW_LpfmDbslbHd4FEQ8E4ZkGBYl3CR6WqfBHRUrXHrCZ4PZzEVjjH5rTTIEApu043c215oNnOJf8KvuLgg1"

def validate_data(df: pd.DataFrame) -> bool:
    
    # Check is no song is downloaded
    if df.empty:
        print("No songs downlaoded!!")
        return False
    
    # Primay key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary key is violated")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found!")

    # Check that all timestamps are within 24 hours
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday:
            raise Exception("At least one of the returned songs does not have a yesterday's timestamp")

    return True

if __name__ == "__main__":

    # Extract part of the ETL process
 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
    
    # Convert time to Unix timestamp in milliseconds      
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000

    # Download all songs you've listened to "after yesterday", which means in the last 24 hours      
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object      
    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    # Prepare a dictionary in order to turn it into a pandas dataframe below       
    song_dict = {
        "song_name" : song_names,
        "artist_name": artist_names,
        "played_at" : played_at_list,
        "timestamp" : timestamps
    }

    song_df = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])

    # Transform part of the ETL process
    if validate_data(song_df):
        print("Data valid, proceed to Load stage")

    # Load part of the ETL process
    # This part saves the extracted and then transformed data into the database. The database could be relational or non-relational.
    # Some of the common relational databases are MySQL, PostgreSQL, SQLite etc.
    # Non-relational database could be MongoDB, Apache Cassandra, DynamoDB, etc.

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")