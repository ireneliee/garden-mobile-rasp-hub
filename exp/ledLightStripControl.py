import RPi.GPIO as GPIO
import time

# Set up GPIO
LED_COUNT = 8
LED_PIN = 18  # GPIO pin connected to the LEDs

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Function to send color data to LEDs
def send_color(color):
    # Send color data to each LED
    for _ in range(LED_COUNT):
        # Send data for each color channel (GRB order)
        for value in color:
            for _ in range(8):
                # Send bit by bit, MSB first
                GPIO.output(LED_PIN, GPIO.HIGH if (value & 0x80) else GPIO.LOW)
                time.sleep(0.0000004)  # 400ns
                GPIO.output(LED_PIN, GPIO.LOW)
                value <<= 1
                time.sleep(0.0000004)  # 400ns

# Turn off all LEDs
send_color((0, 0, 0))

# Turn on each LED with a different color
while True:
    send_color(RED)
    time.sleep(0.5)
    send_color(GREEN)
    time.sleep(0.5)
    send_color(BLUE)

# # Clean up GPIO
# GPIO.cleanup()