import time

import board
import sqlite3
from adafruit_bme280 import basic as adafruit_bme280

i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
conn = sqlite3.connect('temperatureHumidity.db')

# Check if the 'temperature' table exists
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='temperatureHumidity'")
table_exists = cursor.fetchone()

if not table_exists:
    conn.execute('''CREATE TABLE temperatureHumidity (
                        id INTEGER PRIMARY KEY,
                        timestamp TEXT,
                        temp REAL,
                        humidity REAL
                    )''')
    print("Created 'temperatureHumidity' table.")
else:
    print("Table 'temperatureHumidity' already exists.")

conn.commit()


try:
    
    while True:

        temperature = bme280.temperature
        humidity = bme280.humidity
        print('Temperature = {0:0.3f} deg C'.format(temperature))
        print('Humidity    = {0:0.2f} %'.format(humidity))
        sql_query = f"INSERT INTO temperatureHumidity ('timestamp', 'temp', 'humidity') VALUES(datetime('now', 'localtime'), {temperature}, {humidity})"
        
        c = conn.cursor()
        c.execute(sql_query)
        conn.commit()
        
        time.sleep(60)
    
except KeyboardInterrupt:
    print("Program terminated!")
    
finally:
    pass
