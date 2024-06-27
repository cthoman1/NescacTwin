from scrape import scrape_athlete_data
from scrape import extract_athlete_id
import sqlite3
from cleaning import event_codes

conn = sqlite3.connect('nescactf.db')
cursor = conn.cursor()
conn.execute('PRAGMA foreign_keys = ON;')


def clear_database():
    conn = sqlite3.connect('nescactf.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = cursor.fetchall()

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table[0]};")

    conn.commit()
    conn.close()
# This just clears the database to avoid duplicates.


def save_to_db(athlete_url):
    name, school, data = scrape_athlete_data(athlete_url)
    athlete_id = extract_athlete_id(athlete_url)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS athletes (
        athlete_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        school TEXT NOT NULL
    );
    ''')
    cursor.execute('''
    INSERT OR IGNORE INTO athletes (athlete_id,name, school)
    VALUES (?,?,?)
    ''', (athlete_id, name, school))

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS race_results ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        athlete_id INTEGER,
        race_date DATE,
        event TEXT,
        result TEXT,
        FOREIGN KEY (athlete_id) REFERENCES athletes (athlete_id)
    )
    ''')
    cursor.execute('SELECT athlete_id FROM athletes WHERE athlete_id = ?', (athlete_id,))
    athlete_id_in_db = cursor.fetchone()[0]
    for race_date, event, result in data:
        cursor.execute('''
           INSERT INTO race_results (athlete_id, race_date, event, result)
           VALUES (?, ?, ?, ?)
           ''', (athlete_id_in_db, race_date, event, result))
    conn.commit()
# This function is designed to take data from the scrape_athlete_data function and put it into the nescactf.db file.
# It creates the race_results table as well as the athletes table.
# The race_results table tabulates race results and the athletes table assigns a key to each athlete in the db.


def update_event_names_to_codes(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Update event codes
    for event_name, event_code in event_codes.items():
        cursor.execute('''
               UPDATE race_results
               SET event = ?
               WHERE event = ?
           ''', (int(event_code), event_name))
    conn.commit()
    conn.close()


def create_event_code_reference_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            event_name TEXT PRIMARY KEY,
            event_code INTEGER NOT NULL
        )
    ''')
    for event_name, event_code in event_codes.items():
        cursor.execute("INSERT OR REPLACE INTO events (event_name, event_code) VALUES (?, ?)", (event_name, int(event_code)))
    conn.commit()
    conn.close()
