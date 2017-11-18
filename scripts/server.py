# Based on the NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
# Modified by Leo Currie (leo.currie@gmail.com)
#
import time
import json
import web
import sys


from neopixel import *
from threading import Lock


# LED strip configuration:
LED_COUNT      = 400     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

haveData = False
frameData = None


urls = (
    '/pixels', 'pixels'
)
app = web.application(urls, globals())

def mutex_processor():
	mutex = Lock()
	def processor_func(handle):
		mutex.acquire()
		try:
			return handle()
		finally:
			mutex.release()
	return processor_func

app.add_processor(mutex_processor())


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()


class pixels:
	def POST(self):
		try:
			data = web.data()
			pixelData = json.loads(data)
			count = len(pixelData["paint"])
			for i in range(0,count):
				p = pixelData["paint"][i]["p"]
				r = pixelData["paint"][i]["r"]
				g = pixelData["paint"][i]["g"]
				b = pixelData["paint"][i]["b"]
				c = Color(r,g,b);
				strip.setPixelColor(p, c)
			strip.show()
			print "Success"
			return '{"outcome": 200}'
		except:
			print "Fail"
			return '{"outcome": 500}'


# Main program logic follows:
if __name__ == '__main__':
	app.run()
