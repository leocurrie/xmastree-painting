import numpy as np
import argparse
import cv2
import json
import urllib
import urllib2

 
print "var pixels = ["
# Iterate through all the pixels
for x in range(0, 400):
	data = {
		"paint": []
	}

	# Turn off all the pixels, except this one - turn it on full white
	for y in range(0,400):
		color = color = {"p":y,"r":0,"g":0,"b":0}
		if (y == x):
			color = {"p":y,"r":255,"g":255,"b":255}
		data["paint"].append(color)
		
	# POST the data to the server
	req = urllib2.Request('http://127.0.0.1:8080/pixels')
	req.add_header('Content-Type', 'application/json')
	response = urllib2.urlopen(req, json.dumps(data))

	# Take a photo using MJPGStreamer
	req = urllib.urlopen('http://127.0.0.1:8090/?action=snapshot')
	
	# Find the co-ordinates of the brightest spot in the photo
	# From https://www.pyimagesearch.com/2014/09/29/finding-brightest-spot-image-using-python-opencv/
	arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
	image = cv2.imdecode(arr,-1) 
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (41, 41), 0)
	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)

	# Print the result
	print "["+str(maxLoc[0])+","+str(maxLoc[1])+"],"

print "];"
