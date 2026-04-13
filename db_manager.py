import sqlite3 
from datetime import datetime

class DBManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_session(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO sessions (start_time) VALUES (?)", (start_time,))
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return session_id
    
    def enter_temp(self, session_id, sensor_name, temp):
        if session_id is None: return
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        print(f"Insertion DB | Session: {session_id} | Capteur: {sensor_name} | Temp: {temp:.2f}")
        cursor.execute("INSERT INTO temperature_readings (session_id, sensor_name, temperature) VALUES (?, ?, ?)", (session_id, sensor_name, temp))
        conn.commit()
        conn.close()
    
    def reading_temp(self, session_id, sensors, limit):
        if not sensors: return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        placeholders = ', '.join('?' for _ in sensors)
        query = f"""
            SELECT sensor_name, temperature, timestamp
            FROM temperature_readings
            WHERE session_id = ? AND sensor_name IN ({placeholders})
            ORDER BY id DESC LIMIT ?
        """
        cursor.execute(query, (session_id, *sensors, limit))
        
        rows = cursor.fetchall()
        conn.close()
        return rows 