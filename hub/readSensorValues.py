import time
import board
from adafruit_bme280 import basic as adafruit_bme280
from gpiozero import MCP3008
from gpiozero import PWMLED
import _thread as thread


from databaseAccess import DatabaseAccess
from constant import  TEMPERATURE, BRIGHTNESS, SALINITY, SOILPH
from util import sendData

def readTemperatureSensor():
	while True:
		try:
			temperature = bme280.temperature
			database.storeData(TEMPERATURE, temperature)
			sendData(TEMPERATURE, temperature)
			print('Temperature is ', str(temperature))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(60)
	

def readBrightnessSensor():
	while True:
		try:
			brightness = photocell.value
			database.storeData(BRIGHTNESS, brightness)
			sendData(BRIGHTNESS, brightness)
			print('Brightness is ', str(brightness))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(10)

def readSalinitySensor():
	while True:
		try:
			salinity = salinityMeter.value
			database.storeData(SALINITY, salinity)
			sendData(SALINITY, salinity)
			print('Salinity is ', str(salinity))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(5)

def readPhSensor():
	while True:
		try:
			ph = phMeter.value * (5.0 / 1024.0 / 6) * 3.5
			database.storeData(SOILPH, ph)
			sendData(SOILPH, ph)
			print('Soil pH is ', str(ph))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)
	

def setup():
	global database, bme280, photocell, salinityMeter, phMeter
	# initialization database
	database = DatabaseAccess()

	# initialize temperature sensor
	i2c = board.I2C()  # uses board.SCL and board.SDA
	bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
	
	# initialize light sensor
	photocell = MCP3008(0)

	# initialize pH sensor
	salinityMeter = MCP3008(1)

	phMeter = MCP3008(2)

	

def main():

	setup()
	thread.start_new_thread(readTemperatureSensor, ())
	thread.start_new_thread(readBrightnessSensor, ())
	thread.start_new_thread(readSalinitySensor, ())
	thread.start_new_thread(readPhSensor, ())
	print('Program running... Press CTRL+C to exit')
	
	
	
	while True:

		try:                       
						
			time.sleep(0.1)
			
		except RuntimeError as error:
			
			print('Error: {}'.format(error.args[0]))
		
		except Exception as error:
			
			print('Error: {}'.format(error.args[0]))
			
		except KeyboardInterrupt: 

			print('Program terminating...')
			break
	

	print('Program exited...')

if __name__ == '__main__':
    
    main()
