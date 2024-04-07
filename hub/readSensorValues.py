import time
import requests
import board
from gpiozero import get_serial
from datetime import datetime
from adafruit_bme280 import basic as adafruit_bme280

from databaseAccess import DatabaseAccess
from constant import  API, TEMPERATURE, TEMPERATURE_, MOISTURE, MOISTURE_, SOILPH, SOILPH_, SALINITY, SALINITY_

# initialization database
database = DatabaseAccess()

# initialization temperature sensor
i2c = board.I2C()  # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

def sendData(dataType, sensorValue):

	url = API.format(api_mapping[dataType])

	api_mapping = {
		TEMPERATURE: "submitTemperatureData",
		MOISTURE: "submitMoistureData",
		SALINITY: "submitSalinityData",
		SOILPH: "submitPhData"
	}

	print('Current time is: ', str(datetime.now().time()))
	data = {
		"identifier": get_serial(),
		"timestamp": datetime.now().time(),
		"value": sensorValue
	}

	response = requests.post(url, data = data)

	if response.status_code == 200:
		print("Data sending to backend is successful!")
	else:
		print("POST request failed with status code: ", response.status_code)

def readTemperatureSensor():
	temperature = bme280.temperature
	database.storeData(TEMPERATURE, temperature)
	sendData(TEMPERATURE, temperature)

try:
	while True:
		readTemperatureSensor()
		time.sleep(60)



except KeyboardInterrupt:
	
	print('********** END')
	