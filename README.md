# Project: Data Modeling with Postgres

## Project description

The goal is to create a Postgres database with tables designed to optimize queries on song play analysis 
for a compagny called Sparkify. I have created a a database schema and ETL pipeline that transfers 
data from files in two local directories into these tables in Postgres using Python and SQL.

I have used a Star schema  consisting of one fact table (songplays) and four dimension tables (users, 
songs, artists, time) for data modeling. This denormalized model will simplify queries on song play and 
will festen aggregations.

I will provide a query and results for song play analysis at the end.

## Project workspace

In addition to the data files in song_data and log_data repositories, the project workspace includes six files:

 1. *test.ipynb* displays the first few rows of each table to check the database.
 2. *create_tables.py* drops and creates tables. You run this file to reset tables before each time you run ETL scripts.
 3. *etl.ipynb* reads and processes a single file from song_data and log_data and loads the data into tables. 
 4. *etl.py* reads and processes files from song_data and log_data and loads them into your tables. 
 5. *sql_queries.py* contains all your sql queries, and is imported into the last three files above.
 6. *README.md* provides discussion on the project.

## Database schema

I have created a star schema consisting of the following tables:

* <b>Fact table</b>
 
 1. songplays - records in log data associated with song plays :
	
	*songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent )*

* <b>Dimension tables</b>
 
 2. users - users in the app : 
	
	*users ( user_id, first_name, last_name, gender, level )*

 3. songs - songs in music database :

	*songs ( song_id, title, artist_id, year, duration )*
 
 4. artists - artists in music database :

	*artists ( artist_id, name, location, latitude, longitude )*

 5. time - timestamps of records in songplays broken down into specific units :

	*time ( start_time, hour, day, week, month, year, weekday )*


## ETL pipeline

 1. First, run *create_tables.py* to create the database schema with all the necessary tables.
 You need to run this script to reset tables.

 2. Run *etl.py* to process the entire datasets and transfer data from json files into tables.

 3. Run *test.ipynb* to confirm your records were successfully inserted into each table.


## Queries and results

<b>Query :</b>  Find the 5 most played songs. Give the title of the song and the name of the artist

```sql

SELECT songs.title, artists.name, COUNT(*) AS count FROM songplays 
JOIN songs ON songplays.song_id = songs.song_id
JOIN artists ON songs.artist_id = artists.artist_id
WHERE songplays.song_id IS NOT NULL 
GROUP BY songs.title, artists.name ORDER BY count DESC
LIMIT 5

```

|    | title                           			 | name                         | count | 
| -- | ----------------------------------------- | ---------------------------- | ------|  
|  1 | Baby Come To Me  						 | Kenny G featuring Daryl Hall |   7   |
|  2 | Tonight Will Be Alright  				 | Lionel Richie      			|   6   |
|  3 | Auguri Cha Cha  							 | Bob Azzam			        |   5   |
|  4 | Streets On Fire (Explicit Album Version)  | Lupe Fiasco     				|   5   |
|  5 | A Higher Place (Album Version) 			 | Tom Petty			        |   4   |








