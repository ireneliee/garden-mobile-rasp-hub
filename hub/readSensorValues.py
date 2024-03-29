import time
from bluetooth import ble

from hub.databaseAccess import DatabaseAccess
import util
from bleuartlib import BleUartDevice
from constant import TEMPERATURE, TEMPERATURE_, MOISTURE, MOISTURE_, SOILPH, SOILPH_, SALINITY, SALINITY_

# CHANGE ACCORDING TO YOUR OWN MICROBIT ADDRESSES
microbit_address = set([])

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
	data_name = data_array[0]
	data_value = float("{:.3f}".format(float(data_array[1])))

	return data_name, data_value
	
def disconnectAllDevices():
	for device in connectedBlueArtDevices:
		device.disconnect()


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
