# Data Modeling with Postgres

This project create an ETL pipeline and allows to analyze statistic investigations of songplay informations of Sparkify.

## Source Data 
For this project log two datasets are required:
- log_data
- song_data
Log files contains songplay events of the users in json format while song_data contains list of songs details.

**Please Note** This data is currently not shared in that public GitHub repository!

## Database Schema
Following are the fact and dimension tables made for this project:

#### Dimension Tables:

**Table:** users
* columns: user_id, first_name, last_name, gender, level

**Table: songs**
* columns: song_id, title, artist_id, year, duration
   
**Table: artists**
* columns: artist_id, name, location, lattitude, longitude

**Table time**
* columns: start_time, hour, day, week, month, year, weekday

#### Fact Table:
**Table: songplays**
* columns: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent


### Project Structure

The project consists of the following scripts;

* `sql_queries.py` contains the sql queries required for creating tables, inserting values, dropping tables, and selecting songs.
* `create_tables.py` imports the relevant create and drop queries from sql_queries.py, and creates the tables neccessary for the particular database.
* `etl.py` takes the log files, and song files from the needed Files

## Run the Project
1. First you need to create the needed tables. By running `create_tables.py`
2. To populate the tables created in the previous step run `etl.py`

To then ensure that the tables are created, and subsequently populated correctly, you can run `test.ipynb`.
