import sqlite3
from datetime import datetime
from gps import gps
import folium

# Connect to the SQLite database
conn = sqlite3.connect('locations.db')
c = conn.cursor()

# Create a table to store location data
c.execute('CREATE TABLE IF NOT EXISTS locations (timestamp TEXT, lat REAL, lon REAL)')

# Initialize the GPS sensor
gpsd = gps(mode=gps.WATCH_ENABLE)

while True:
    # Read the GPS data
    report = gpsd.next()
    
    # If the data is valid, store it in the database
    if report['class'] == 'TPV':
        lat = report.lat
        lon = report.lon
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('INSERT INTO locations VALUES (?, ?, ?)', (timestamp, lat, lon))
        conn.commit()
        
        # Visualize the data on a map
        m = folium.Map(location=[lat, lon], zoom_start=16)
        folium.Marker([lat, lon]).add_to(m)
        m.save('map.html')
