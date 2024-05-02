
import time
from adafruit_bme280 import basic as adafruit_bme280
# from picamera2 import Picamera2, Preview
from gpiozero import MCP3008
from gpiozero import PWMLED
import serial
import RPi.GPIO as GPIO
import busio
import adafruit_blinka.board as board
import _thread as thread
import neopixel
import board
from picamera2 import Picamera2, Preview
from util import sendPicture

from databaseAccess import DatabaseAccess

from constant import TEMPERATURE, BRIGHTNESS, SALINITY, SOILPH, MOISTURE, LOW_TEMPERATURE_THRESHOLD, LOW_LIGHT_THRESHOLD, LOW_PH_THRESHOLD, IDEAL_TEMPERATURE_VALUES, IDEAL_SALINITY_VALUES, IDEAL_MOISTURE_VALUES, IDEAL_PH_VALUES, IDEAL_BRIGHTNESS_VALUES
from util import sendData, retrieveIdealValues, sendPicture
from moistureSerial import readMoistureSensor

def sendCommand(command):
        
    command = command + '\n'
    ser.write(str.encode(command))
    
def waitResponse():
    
    response = ser.readline()
    response = response.decode('utf-8').strip()
    
    return response

def getIdeal():
    # get ideal from server here
    ideal = 500
    return ideal
    
def readMoistureSensor():

    database = DatabaseAccess()
    
    global ser
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1)
    print('rhub: Listening on /dev/ttyACM0... Press CTRL+C to exit')
    
    while True:
                
        time.sleep(3)                    
            
        commandToTx = 'ideal=' + str(getIdeal())           
        sendCommand('cmd:' + commandToTx)                    
                        
        if commandToTx.startswith('ideal='):
                    
            strSensorValues = ''
                            
            while strSensorValues == None or len(strSensorValues) <= 0:
                        
                strSensorValues = waitResponse()
                time.sleep(1)

                listSensorValues = strSensorValues.split(',')

                for sensorValue in listSensorValues:
                    value = sensorValue
                    print('rhub: {}'.format(sensorValue))
                        
                if value != "":
                    moistureData = int(value)
                    database.storeData(MOISTURE, moistureData)
                    sendData(MOISTURE, moistureData)

def readTemperatureSensor():
	while True:
		try:
			temperature = bme280.temperature
			print('Temperature is ', str(temperature))
			if temperature < ideal_temperature_value - LOW_TEMPERATURE_THRESHOLD:
				
				print('Temperature level is too low.')
				turn_on()
			else:
				turn_off()
			database.storeData(TEMPERATURE, temperature)
			sendData(TEMPERATURE, temperature)
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(5)
def readBrightnessSensor():
	while True:
		try:
			brightness = photocell.value * 5.0

			if brightness < ideal_brightness_value - LOW_LIGHT_THRESHOLD:
				print('Brightness level is too low.')
				print('Actuation: turn on')
				turn_on()
			else:
				print('Actuation: turn off')
				turn_off()

			database.storeData(BRIGHTNESS, brightness)
			sendData(BRIGHTNESS, brightness)
			print('Brightness is ', str(brightness))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(5)

def readSalinitySensor():
	while True:
		try:
			salinity = salinityMeter.value * 5.0

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
			voltage = phMeter.value * 5.0
			ph = 7.0 + (voltage - 2.5)

			database.storeData(SOILPH, ph)
			sendData(SOILPH, ph)
			print('Soil pH is ', str(ph))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(5)
   
# def takePicture():
# 	while True:
# 		try:
# 			picam2 = Picamera2()
# 			camera_config = picam2.create_still_configuration()
# 			picam2.configure(camera_config)
# 			picam2.start()
# 			time.sleep(2)
# 			picam2.capture_file("/home/pi/Desktop/gardenPicture.jpg")
# 			sendPicture("/home/pi/Desktop/gardenPicture.jpg")
# 			print('Sent Picture')
# 		except Exception as e:
# 			print("An error occurred: ", e)
# 		finally:
# 			time.sleep(2)
def setup():
	global database, bme280, photocell, salinityMeter, phMeter, ideal_temperature_value, ideal_brightness_value, ideal_moisture_value
	# initialization database
	database = DatabaseAccess()

	# Define I2C pins (replace with actual pin numbers)
	scl_pin = 3
	sda_pin = 2
	# Create I2C bus
	i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
	# Initialize BME280 sensor
	bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
	
	# initialize light sensor
	photocell = MCP3008(1)

	# initialize pH sensor
	salinityMeter = MCP3008(2)

	phMeter = MCP3008(0)

	ideal_temperature_value = IDEAL_TEMPERATURE_VALUES
	ideal_brightness_value = IDEAL_BRIGHTNESS_VALUES
	ideal_moisture_value = IDEAL_MOISTURE_VALUES

def setupLed():
	global pixels1, currentState
	pixels1 = neopixel.NeoPixel(board.D18, 55, brightness=1)
	currentState = False

def maintainLed():
	global pixels1, currentState
	while True:
		try:
			if currentState:
				pixels1.fill((0, 220, 0))
			else:
				pixels1.fill((0, 0, 0))

		except Exception as e:
			print("An error occurred while maintaining LED: ", e)
		finally:
			time.sleep(0.1)

def turn_on():
	global currentState
	currentState = True

def turn_off():
	global currentState
	currentState = False
	
def updateIdealValues():
	global ideal_temperature_value, ideal_moisture_value
	while True:

		try:
			ideal_values = retrieveIdealValues()
			if ideal_values:
				ideal_temperature_value = ideal_values["ideal_temp_level"]
				ideal_moisture_value = ideal_values["ideal_moisture_level"]
		

		except Exception as e:
			print("An error occurred while retrieving ideal value: ", e)
		finally:
			time.sleep(5)

def takePicture():
	while True:
		try:
			picam2 = Picamera2()
			camera_config = picam2.create_still_configuration()
			picam2.configure(camera_config)
			picam2.start()
			time.sleep(2)
			picam2.capture_file("/home/pi/Desktop/gardenPicture.jpg")
			sendPicture("/home/pi/Desktop/gardenPicture.jpg")
			print('Sent Picture')
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)
		
def main():

	setup()
	setupLed()
	thread.start_new_thread(readTemperatureSensor, ())
	thread.start_new_thread(readSalinitySensor, ())
	thread.start_new_thread(readBrightnessSensor, ())
	thread.start_new_thread(readPhSensor, ())
	thread.start_new_thread(readMoistureSensor,())
	thread.start_new_thread(maintainLed,())
	thread.start_new_thread(takePicture, ())
	thread.start_new_thread(updateIdealValues, ())
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
	pixels1.fill((0, 0, 0))
	

if __name__ == '__main__':
    
    main()