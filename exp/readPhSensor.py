import time
import board
from adafruit_bme280 import basic as adafruit_bme280
from gpiozero import MCP3008
from gpiozero import PWMLED

phMeter = MCP3008(0)
tdsSensor = MCP3008(1)

while True:
	try:
		voltage = phMeter.value * 5
		ph = 7 + (2.5 - voltage)
		print('Soil pH is ', str(ph))
		tdsValue = tdsSensor.value * 5
		print('TDS value is ', str(tdsValue))
	except Exception as e:
		print("An error occurred: ", e)
	finally:
			time.sleep(2)