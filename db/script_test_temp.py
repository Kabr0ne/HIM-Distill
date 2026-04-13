import sqlite3
import time
import random

DB_PATH = 'him_distill.db'

def get_latest_session_id():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM sessions")
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else None
    except Exception as e:
        print(f"Erreur lecture session : {e}")
        return None

def insert_temp(session_id, name, temp):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO temperature_readings (session_id, sensor_name, temperature) 
        VALUES (?, ?, ?)
    """, (session_id, name, temp))
    conn.commit()
    conn.close()

sensors = ["T1", "T2", "T3", "T4"]

try:
    while True:
        s_id = get_latest_session_id()
        
        if s_id is None:
            time.sleep(5)
            continue

        for c in sensors:
            temp = random.uniform(20.0, 100.0)
            insert_temp(s_id, c, temp)
            print(f"[Session {s_id}] {c} : {temp:.2f}°C")
            
        time.sleep(5)
except KeyboardInterrupt:
    print("Simulation arrêtée.")