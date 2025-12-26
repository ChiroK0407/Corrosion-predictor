# database/corrosion_db.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "corrosion_data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS corrosion_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            lat REAL,
            lon REAL,
            temperature REAL,
            humidity REAL,
            wind_speed REAL,
            description TEXT,
            SO2 REAL,
            NO2 REAL,
            PM2_5 REAL,
            PM10 REAL,
            substrate TEXT,
            corrosion_rate REAL
        )
    """)
    conn.commit()
    conn.close()

def insert_record(lat, lon, weather, pollution, substrate, corrosion_rate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO corrosion_records (
            lat, lon, temperature, humidity, wind_speed, description,
            SO2, NO2, PM2_5, PM10, substrate, corrosion_rate
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lat, lon,
        weather["temperature"], weather["humidity"], weather["wind_speed"], weather["description"],
        pollution["SO2"], pollution["NO2"], pollution["PM2_5"], pollution["PM10"],
        substrate, corrosion_rate
    ))
    conn.commit()
    conn.close()