# Project: Data Modeling with Postgres

## Project description

The goal is to create a Postgres database with tables designed to optimize queries on song play analysis 
for a compagny called Sparkify. I have created a a database schema and ETL pipeline that that transfers 
data from files in two local directories into these tables in Postgres using Python and SQL.

I will provide some queries and results for song play analysis at the end.

## Project workspace

In addition to the data files in song_data and log_data repositories, the project workspace includes six files:

 1. test.ipynb displays the first few rows of each table to check the database.
 2. create_tables.py drops and creates tables. You run this file to reset tables before each time you run ETL scripts.
 3. etl.ipynb reads and processes a single file from song_data and log_data and loads the data into tables. 
 4. etl.py reads and processes files from song_data and log_data and loads them into your tables. 
 5. sql_queries.py contains all your sql queries, and is imported into the last three files above.
 6. README.md provides discussion on the project.

## Database schema

I have created a star schema consisting of the following tables:

* Fact table
 
 1. songplays - records in log data associated with song plays :
	
	songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent )

* Dimension tables
 
 2. users - users in the app : 
	
	users ( user_id, first_name, last_name, gender, level )

 3. songs - songs in music database :

	songs ( song_id, title, artist_id, year, duration )
 
 4. artists - artists in music database :

	artists ( artist_id, name, location, latitude, longitude )

 5. time - timestamps of records in songplays broken down into specific units :

	time ( start_time, hour, day, week, month, year, weekday )


## ETL pipeline

 1. First, run create_tables.py to create the database schema with all the necessary tables.
 You need to run this script to reset tables.

 2. Run etl.py to process the entire datasets and transfer data from json files into tables.

 3. Run test.ipynb to confirm your records were successfully inserted into each table.


## Queries and results

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.