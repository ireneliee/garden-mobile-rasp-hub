from picamera2 import Picamera2, Preview
from util import sendPicture
import _thread as thread

import time
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
	GPIO.cleanup()

if __name__ == '__main__':
    
    main()