import time
from bluetooth import ble

from databaseAccess import DatabaseAccess
import util
from bleuartlib import BleUartDevice
from constant import microbit_address, TEMPERATURE, TEMPERATURE_, MOISTURE, MOISTURE_, SOILPH, SOILPH_, SALINITY, SALINITY_



connectedBlueArtDevices = []

database = DatabaseAccess()

def addBleUartDevice(address):
	bleUartDevice = BleUartDevice(address)
	bleUartDevice.connect()
	bleUartDevice.enable_uart_receive(bleUartReceiveCallback)
	
	connectedBlueArtDevices.append(bleUartDevice)

def bleUartReceiveCallback(data):
	print('Received data = {}'.format(data))
	tableName, sensorValue = parseReceivedData(data)
	database.storeData(tableName, sensorValue)

def parseReceivedData(data):
	data_array = data.split(":")
	data_name = removeNullChars(data_array[0])
	data_value = float("{:.3f}".format(float(data_array[1])))

	mapping = {
		TEMPERATURE_: TEMPERATURE,
		SOILPH_ : SOILPH,
		SALINITY_: SALINITY,
		MOISTURE_: MOISTURE
	}
	
	print(data_name)
	print(data_value)

	return mapping[data_name], data_value
	
def disconnectAllDevices():
	for device in connectedBlueArtDevices:
		device.disconnect()

def removeNullChars(input_string):
    return input_string.replace('\x00', '')
    
try:

	service = ble.DiscoveryService()
	devices = service.discover(10)

	print('********** Initiating device discovery......')

	for address,name in devices.items():
		if address in microbit_address:
			print('Found BBC micro:bit: {}'.format(address))
			addBleUartDevice(address)
			print('Added the microbit...')

	if len(connectedBlueArtDevices) > 0:
		while True:
			time.sleep(0.1)

except KeyboardInterrupt:
	
	print('********** END')
	
except:

	print('********** UNKNOWN ERROR')

finally:

	disconnectAllDevices()
