import requests

from constant import  API, TEMPERATURE,  MOISTURE,  SOILPH, SALINITY
from datetime import datetime

def getSerialNumber():
    serial = None
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if line.startswith('Serial'):
                serial = line.split(':')[1].strip()
                break
    return serial

def sendData(dataType, sensorValue):
	api_mapping = {
		TEMPERATURE: "submitTemperatureData",
		MOISTURE: "submitMoistureData",
		SALINITY: "submitSalinityData",
		SOILPH: "submitPhData"
	}

	url = API.format(api_mapping[dataType])
	
	print('Current time is: ', str(datetime.now().time()))
	data = {
		"identifier": getSerialNumber(),
		"timestamp": datetime.now().time(),
		"value": sensorValue
	}

	response = requests.post(url, data = data)

	if response.status_code == 200:
		print("Data sending to backend is successful!")
	else:
		print("POST request failed with status code: ", response.status_code)
