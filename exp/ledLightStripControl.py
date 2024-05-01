import board
import neopixel
import digitalio

# Configuration
LED_COUNT = 8
LED_PIN = board.D10
ORDER = neopixel.GRB 

led_pin = digitalio.DigitalInOut(LED_PIN)
led_pin.switch_to_output()

pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, pixel_order=ORDER, auto_write=False)

pixels.brightness = 0.1

pixels[0] = (255, 0, 0)
pixels[1] = (255, 0, 0)


pixels.show()
