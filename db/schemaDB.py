import sqlite3

def init_db():
    connection = sqlite3.connect('him_distill.db')
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_time DATETIME
        )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS temperature_readings 
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            sensor_name TEXT NOT NULL,
            temperature REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()