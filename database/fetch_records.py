# database/fetch_records.py

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "corrosion_data.db")

def fetch_all_records(limit=10):
    """Fetch the most recent corrosion records."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, lat, lon, temperature, humidity, wind_speed,
               SO2, NO2, PM2_5, PM10, substrate, corrosion_rate
        FROM corrosion_records
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_by_substrate(substrate):
    """Fetch records filtered by substrate type."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, lat, lon, temperature, humidity, wind_speed,
               SO2, NO2, PM2_5, PM10, substrate, corrosion_rate
        FROM corrosion_records
        WHERE substrate = ?
        ORDER BY timestamp DESC
    """, (substrate,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    print("📊 Latest Records:")
    records = fetch_all_records(limit=5)
    for r in records:
        print(r)

    print("\n🔩 Records for carbon_steel:")
    steel_records = fetch_by_substrate("carbon_steel")
    for r in steel_records:
        print(r)