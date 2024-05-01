# backend api
# change the api to your own ip address
API = "http://127.20.10.12:5000/data/{}"

DATABASE_NAME = "gardenBuddyData.db"
# long form
TEMPERATURE = "temperature"
MOISTURE = "moisture"
SALINITY = "salinity"
SOILPH = "soilPh"
BRIGHTNESS = "brightness"
HEIGHT = "height"

# short form
TEMPERATURE_ = "temp"
MOISTURE_ = "mois"
SALINITY_ = "sali"
SOILPH_ = "soil"

# sensor data sending format
sensor_data_format = "{}:{}"

# default sensor threshold for actions
LOW_TEMPERATURE_THRESHOLD = 30
HIGH_TEMPERATURE_THRESHOLD = 50

LOW_SALINITY_THRESHOLD = 0.1
LOW_PH_THRESHOLD = 7.0
LOW_LIGHT_THRESHOLD = 0.1

# LED lights customization
TEMPERATURE_TOO_LOW = (255, 0, 0)
TEMPERATURE_TOO_HIGH = (0, 0, 255)
LIGHT_TOO_LOW = (255, 255, 255)


