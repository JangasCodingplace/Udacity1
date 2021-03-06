import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Load Song File and extract song- and artist informations
    It stores this information into the respective songs and artists table
    
    INPUTS:
        * `cur`: cursor variable of database
        * `filepath`: file path to song file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = song_data.iloc[0].values.tolist()
    
    try:
        song_data[3] = int(song_data[3])
    except ValueError:
        song_data[3] = None
    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = artist_data.iloc[0].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Load Log File and extract songplay log- and user informations.
    It stores this information into the respective songplays and user table
    
    INPUTS:
        * `cur`: cursor variable of database
        * `filepath`: file path to song file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [
        [
            row[1],
            row[1].hour,
            row[1].day,
            row[1].week,
            row[1].month,
            row[1].year,
            row[1].weekday()
        ] for row in t.items()
    ]
    column_labels = ('timestamp', 'hour', 'day', 'week', 'month', 'year', 'weekday') 
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            index, pd.to_datetime(row['ts']), row['userId'], row['level'], songid, artistid, row['sessionId'], row['location'], row['userAgent']
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Takes in the path of a root directory that contains the json files
    and the function that processes each individual file.
    
    First it extracts a list of all the json files in the given directory.
    Then it iterates over that list and passes each file to the function that processes the file.
    
    INPUTS:
        * `cur`: cursor variable of database
        * `conn`: connection variable of database
        * `filepath`: path of the root directory to process
        * `func`: function which processes each file
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()