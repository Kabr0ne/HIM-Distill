import sqlite3
import time
import random

def insert_temp(name, temp):
    connection = sqlite3.connect('him_distill.db')
    cursor = connection.cursor()

    cursor.execute("INSERT INTO temperature_readings (sensor_name, temperature) VALUES (?, ?)", (name, temp))
    connection.commit()
    connection.close()

sensor = ["T1", "T2", "T3", "T4"]

try:
    while True:
        for c in sensor:
            temp = random.uniform(20.0, 100.0)
            insert_temp(c, temp)
            print(f"Inserted {temp:.2f}°C for {c}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopped inserting temperature readings.")