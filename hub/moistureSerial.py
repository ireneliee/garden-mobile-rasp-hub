import time

import serial

from util import sendData

from databaseAccess import DatabaseAccess

from constant import MOISTURE

import _thread as thread


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
            
        commandToTx = 'ideal=' + getIdeal()                
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
                        

def main():
    
    thread.start_new_thread(readMoistureSensor, ())
    
    print('Program running... Press CTRL+C to exit')
    
    while True:

        try:                       
                        
            time.sleep(0.1)
            
        except RuntimeError as error:
            
            print('Error: {}'.format(error.args[0]))
        
        except Exception as error:
            
            print('Error: {}'.format(error.args[0]))
            
        except KeyboardInterrupt:                  
        
            if ser.is_open:
            
                ser.close()                           
                    
            print('Program terminating...')
            
            break
    

    print('Program exited...')
    
if __name__ == '__main__':
    
    main()
            

            
