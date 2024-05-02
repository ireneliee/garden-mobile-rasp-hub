import requests

from constant import  API, TEMPERATURE,  MOISTURE,  SOILPH, SALINITY, BRIGHTNESS, HEIGHT
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
		SOILPH: "submitPhData",
		BRIGHTNESS: "submitBrightnessData",
        HEIGHT: "submitHeightData"
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

def retrieveIdealValues():
    url = API.format("getGardenTypeBySerialId") + "?serialId=" + getSerialNumber()
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        print('Error:', response.status_code)
        return None

def sendPicture(picture_path):
    url = API.format("submitPictureData")

    try:
        with open(picture_path, 'rb') as file:
            files = {'file': file}
            data = {
                "identifier": getSerialNumber(),
                "timestamp": str(datetime.now().time())
            }
            response = requests.post(url, files=files, data=data)

            if response.status_code == 200:
                print("Picture sending to backend is successful!")
            else:
                print("POST request failed with status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)