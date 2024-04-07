import time
import board
from adafruit_bme280 import basic as adafruit_bme280


from databaseAccess import DatabaseAccess
from constant import  TEMPERATURE
from util import sendData

def readTemperatureSensor():
	temperature = bme280.temperature
	database.storeData(TEMPERATURE, temperature)
	sendData(TEMPERATURE, temperature)

# initialization database
database = DatabaseAccess()

# initialization temperature sensor
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

try:
	while True:
		try:
			readTemperatureSensor()
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(60)

except KeyboardInterrupt:
	
	print('********** END')