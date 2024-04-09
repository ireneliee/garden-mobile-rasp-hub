

import time

from bluetooth import ble



from util import sendData

from bleuartlib import BleUartDevice

from databaseAccess import DatabaseAccess

from constant import  MOISTURE





def readMoistureSensor():

    database = DatabaseAccess()

    

    def bleUartReceiveCallback(data):

        print(f'Received data = {data}')

        formatted_data = data.replace('\0', '')

        database.storeData(MOISTURE, formatted_data)

        sendData(MOISTURE, formatted_data)

     

    try:



        bleUartDevice1 = None

        found_microbit = False



        service = ble.DiscoveryService()

        devices = service.discover(2)



        print('********** Initiating device discovery......')



        for address,name in devices.items():



            found_microbit = False


            # Change address to microbit address
            if address == 'DC:D4:D5:8C:81:0F':



                print('Found BBC micro:bit [povov]: {}'.format(address))

                found_microbit = True

                break

            

            elif address == 'EA:7D:2B:94:D2:86':

                

                print('Found BBC micro:bit [tagup]: {}'.format(address))

                found_microbit = True

                break
            
            else:
                print('No microbit found')
                break

        if found_microbit:



            bleUartDevice1 = BleUartDevice(address)

            bleUartDevice1.connect()

            print('Connected to micro:bit device')

            

            data = bleUartDevice1.enable_uart_receive(bleUartReceiveCallback)

            print('Receiving data...')



            while True:

                time.sleep(0.1)



    except KeyboardInterrupt:

        

        print('********** END')

        

    except:



        print('********** UNKNOWN ERROR')



    finally:



        if bleUartDevice1 != None:

            

            bleUartDevice1.disconnect()

            bleUartDevice1 = None

            print('Disconnected from micro:bit device')

            

    

    

