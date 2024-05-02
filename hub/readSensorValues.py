import time
import board
from adafruit_bme280 import basic as adafruit_bme280
from picamera2 import Picamera2, Preview
from gpiozero import MCP3008
from gpiozero import PWMLED
import _thread as thread

from databaseAccess import DatabaseAccess

from constant import TEMPERATURE, BRIGHTNESS, SALINITY, SOILPH, LOW_SALINITY_THRESHOLD, LOW_TEMPERATURE_THRESHOLD, HIGH_TEMPERATURE_THRESHOLD, LOW_LIGHT_THRESHOLD, LOW_PH_THRESHOLD, TEMPERATURE_TOO_HIGH, TEMPERATURE_TOO_LOW, LIGHT_TOO_LOW
from util import getSerialNumber, sendData, sendPicture
from moistureSerial import readMoistureSensor

def sendNotification(message):
	print('Notification sent: ', str(message))
	pass


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
			
			# if temperature < LOW_TEMPERATURE_THRESHOLD:
			# 	sendNotification("Temperature level is too low")
			# 	turnOnLed(TEMPERATURE_TOO_LOW)
			# elif temperature > HIGH_TEMPERATURE_THRESHOLD:
			# 	sendNotification("Temperature level is too high")
			# 	turnOnLed(TEMPERATURE_TOO_HIGH)
			# 	turnOnLed(TEMPERATURE_TOO_HIGH)
			# else:
			# 	turnOffLed
				
			database.storeData(TEMPERATURE, temperature)
			sendData(TEMPERATURE, temperature)
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)
	
	
def readBrightnessSensor():
	while True:
		try:
			brightness = photocell.value * 5.0

			# if brightness < LOW_LIGHT_THRESHOLD:
			# 	sendNotification("Brightness level is too low.")
			# 	turnOnLed(LIGHT_TOO_LOW)
			# else:
			# 	turnOffLed

			database.storeData(BRIGHTNESS, brightness)
			# sendData(BRIGHTNESS, brightness)
			print('Brightness is ', str(brightness))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)

def readSalinitySensor():
	while True:
		try:
			salinity = salinityMeter.value * 5.0

			# if salinity < LOW_SALINITY_THRESHOLD:
			# 	sendNotification("Salinity level is too low.")

			database.storeData(SALINITY, salinity)
			sendData(SALINITY, salinity)
			print('Salinity is ', str(salinity))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)

def readPhSensor():
	while True:
		try:
			voltage = phMeter.value * 5.0
			ph = 7.0 + (voltage - 2.5)

			# if ph < LOW_PH_THRESHOLD:
			# 	sendNotification("pH level is too low.")

			database.storeData(SOILPH, ph)
			sendData(SOILPH, ph)
			print('Soil pH is ', str(ph))
		except Exception as e:
			print("An error occurred: ", e)
		finally:
			time.sleep(2)
   
def takePicture():
	while True:
		try:
			picam2 = Picamera2()
			camera_config = picam2.create_still_configuration()
			picam2.configure(camera_config)
			picam2.start()
			time.sleep(2)
			serial_number = getSerialNumber()
			picam2.capture_file("/home/pi/Desktop/gardenPicture.jpg")
			sendPicture("/home/pi/Desktop/gardenPicture.jpg")
			print('Sent Picture')
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
	photocell = MCP3008(1)

	# initialize pH sensor
	salinityMeter = MCP3008(2)

	phMeter = MCP3008(0)




def main():

	setup()
	thread.start_new_thread(readTemperatureSensor, ())
	thread.start_new_thread(readBrightnessSensor, ())
	thread.start_new_thread(readSalinitySensor, ())
	thread.start_new_thread(readPhSensor, ())
	thread.start_new_thread(readMoistureSensor,())
	thread.start_new_thread(takePicture, ())
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

