import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from pandas import DataFrame 


def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)
    
    # insert song record
    song_df = pd.DataFrame(df, columns=['song_id', 'title','artist_id','year','duration'])
    song_data = song_df.values.flatten()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_df = pd.DataFrame(df, columns=['artist_id', 'artist_name','artist_location','artist_longitude','artist_latitude'])
    artists_df = artist_df.rename(columns={
        "artist_name" : "name",
        "artist_location" : "location",
        "artist_longitude" : "longitude",
        "artist_latitude" : "latitude"
        })
    artist_data = artist_df.values.flatten()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)
   
    # filter by NextSong action
    df = df[df.song.notnull()]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [
        t.apply(lambda x: x.strftime('%X')),
        t.apply(lambda x: x.strftime('%H')),
        t.apply(lambda x: x.strftime('%d')),
        t.apply(lambda x: x.strftime('%W')),
        t.apply(lambda x: x.strftime('%m')),
        t.apply(lambda x: x.strftime('%Y')),
        t.apply(lambda x: x.strftime('%w'))
    ]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, column_labels)
    # I transpose time_df 
    time_df = time_df.T

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame(df, columns=['userId', 'firstName','lastName','gender','level'])
    user_df = user_df.rename(columns={
        "userId" : "user_id",
        "firstName" : "first_name",
        "lastName" : "last_name"
        })

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        #songid, artistid = results if results else None, None
        # Destructing does not work properly here for unknown reason

        if results:
            songid = results[0] 
            artistid = results[1]
        else:
            songid = None
            artistid = None
        
        
        # insert songplay record
        songplay_data = [row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
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