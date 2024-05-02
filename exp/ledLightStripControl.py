import RPi.GPIO as GPIO
import time
LED_COUNT = 8
LED_PIN = 18  # GPIO pin connected to the LEDs

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def turn_on(color):
    for _ in range(LED_COUNT):
        send_bit(GPIO.HIGH if color else GPIO.LOW)

def turn_off():
    for _ in range(LED_COUNT):
        send_bit(GPIO.LOW)

def send_bit(value):
    GPIO.output(LED_PIN, value)
    GPIO.output(LED_PIN, GPIO.HIGH)  # Pulse high to latch data
    GPIO.output(LED_PIN, GPIO.LOW)

# Example usage
turn_on(GPIO.HIGH)  # Turn on with color (you can adjust color as needed)
time.sleep(10)
GPIO.cleanup()