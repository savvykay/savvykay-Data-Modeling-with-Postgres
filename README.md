<<<<<<< HEAD
# Data-Modeling-with-Postgres
Udacity Data Engineering Nanodegree - Project 1 - Data modeling with PostgreSQL. Creating a Database and ETL pipeline in Postgres for a music streaming app.
=======
# Sparkify ETL Project

## Project Overview

Sparkify, a startup in the music streaming industry, seeks to analyze the data they've been collecting on user activity and song metadata. The goal is to understand user behavior, such as which songs are being played the most. However, the raw data exists in JSON files, making it difficult to query efficiently.

As a data engineer, your role is to design a Postgres database schema optimized for analytical queries and implement an ETL pipeline to populate the database with data extracted from the JSON files. This project enables Sparkify's analytics team to perform in-depth song play analysis.

---
## Requirements
This project requires the following:
- `Pandas` 
- `psycopg2`
- PosgreSQL database on localhost

---

## How to Run the Python Scripts

To run the ETL pipeline, follow these steps:

1. Open a terminal or command prompt.
2. Run the following:
   python create_tables.py
   python etl.py
   
To do this within Jupyter, go to New > Terminal

---


## Repository Contents

The repository includes the following files:

1. **`test.ipynb`**  
   - A Jupyter Notebook to test the database and view the first few rows of each table.

2. **`create_tables.py`**  
   - A Python script to reset the database by dropping and recreating the tables. Run this script before executing the ETL pipeline.

3. **`etl.ipynb`**  
   - A Jupyter Notebook that demonstrates the ETL process step-by-step for a single JSON file. It provides a detailed guide to the ETL logic.

4. **`etl.py`**  
   - The main ETL pipeline script. This script processes all the JSON files in the `data/song_data` and `data/log_data` directories and loads the data into the database. Comments are included for each function to explain what it does.

5. **`sql_queries.py`**  
   - Contains all SQL queries, including `DROP`, `CREATE`, `INSERT`, and `SELECT` statements. These are imported and used in the other scripts.

6. **`README.md`**  
   - Provides an overview of the project, its purpose, and instructions for usage.

---

## Database Schema Design

The database follows a star schema design, which optimizes query performance for analytical tasks. This schema includes:

### Fact Table
- **songplays**  
  - Records song play events by combining data from song and log files.

### Dimension Tables
- **users**  
  - Contains user demographic information (e.g., user ID, name, gender, subscription level).
- **songs**  
  - Stores song information (e.g., song ID, title, artist, duration).
- **artists**  
  - Contains artist details (e.g., artist ID, name, location, latitude, longitude).
- **time**  
  - Captures time-related data, such as timestamps, hour, day, week, month, year, and weekday.

### Why Star Schema?
This design simplifies queries by organizing data into fact and dimension tables, reducing redundancy and improving query efficiency.

---

## ETL Pipeline

The ETL process is implemented in `etl.py` and includes the following steps:

### Extract
- Parse JSON files from `data/song_data` and `data/log_data`.

### Transform
- Process and clean the extracted data. For example:
  - Extract song and artist details for the songs and artists tables.
  - Convert timestamps and extract time-related fields for the time table.
  - Query the songs and artists tables to populate the songplays fact table.

### Load
- Insert the transformed data into the respective tables in the `sparkifydb` database.

---

## Example Query

An example of a query that could be run with these new database tables would be most played songs:

```sql
SELECT s.title, COUNT(sp.song_id) AS play_count
FROM songplays sp
JOIN songs s ON sp.song_id = s.song_id
GROUP BY s.title
ORDER BY play_count DESC
LIMIT 10;
```

---


>>>>>>> 71b98f2 (Add project files including notebook, scripts, and data)
