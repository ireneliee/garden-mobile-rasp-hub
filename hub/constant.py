# backend api
# change the api to your own ip address
API = "http://172.25.97.217:5000/data/{}"

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

# default sensor ideal values
IDEAL_TEMPERATURE_VALUES = 20
IDEAL_SALINITY_VALUES = 10.0
IDEAL_MOISTURE_VALUES = 500
IDEAL_PH_VALUES = 7
IDEAL_BRIGHTNESS_VALUES = 2.0

LOW_SALINITY_THRESHOLD = 0.1
LOW_PH_THRESHOLD = 7.0
LOW_LIGHT_THRESHOLD = 0.1
LOW_TEMPERATURE_THRESHOLD = 5


