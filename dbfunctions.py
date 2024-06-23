from scrape import scrape_athlete_data
import sqlite3


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


clear_database()


def save_to_db(athlete_id):
    name, school, data = scrape_athlete_data(athlete_id)
    # print(f"Scraped data for athlete_id {athlete_id}: {name}, {school}, {data}")
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


