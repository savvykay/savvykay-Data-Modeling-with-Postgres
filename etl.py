import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

def get_files(filepath):
    """
    Gets the JSON files from a given directory/subdirectories.

    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))
    return all_files

def process_song_file(cur, filepath):
    """
    Processes a song file to insert records into the songs and artists tables.
    """
    # Load song file
    df = pd.read_json(filepath, lines=True)

    # Insert song record
    song_data = list(df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """
    Processes a single log file to insert records into the time, users, and songplays tables.
    
    """
    # Log file
    df = pd.read_json(filepath, lines=True)

    # Filter to NextSong
    df = df[df['page'] == 'NextSong']

    # Convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # Insert time data records
    time_data = {
        'start_time': df['ts'],
        'hour': df['ts'].dt.hour,
        'day': df['ts'].dt.day,
        'week': df['ts'].dt.week,
        'month': df['ts'].dt.month,
        'year': df['ts'].dt.year,
        'weekday': df['ts'].dt.day_name()
    }
    time_df = pd.DataFrame(time_data)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # Insert user records
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # Insert songplay records
    for index, row in df.iterrows():
        # Get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # Insert songplay record
        songplay_data = (
            row.ts, row.userId, row.level, songid, artistid, 
            row.sessionId, row.location, row.userAgent
        )
        cur.execute(songplay_table_insert, songplay_data)

def process_data(cur, conn, filepath, func):
    """
    Processes all files in a given directory using the provided processing function.
    
    """
    all_files = get_files(filepath)
    print(f'{len(all_files)} files found in {filepath}')

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print(f'{i}/{len(all_files)} files processed.')

def main():
    """
    Main function to connect to the database and process song and log data.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

if __name__ == "__main__":
    main()
