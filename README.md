# xmastree-painting
The idea behind the project is that a user can 'paint' colour onto a christmas tree like using 'paint' on a PC.
The project is made from several different software and hardware components.

## Hardware

Hardware wise, the project was implemented with several strings of WS2812 LEDs. These are commonly sold in strings of 50.
The strings were daisy-chained together, with appropriate power supply arrangements. The data input to the string was fed directly from a Raspberry Pi.
Although the specs say that the WS2812 requires a 5V signal, the 3.3v signal from the RPi seemed to work fine.
The video camera used was a Raspberry Pi camera.

The project could certainly be implemented with different hardware - for example, most modern USB webcams are able to deliver MJPG streams and thus could be used in place of the Raspberry Pi webcam.
An Arduino, or even an ESP8266 module could be used to implement the server.

## Software

There are 4 components

1. An HTTP server (the "Pixel Server") to control a string of WS2811/WS2812 LEDs.
   The Pixel Server handles JSON messages posted from the UI. These messages simply contain an array of pixel colours, there is one array element for each LED of interest. The pixel colours are passed as RGB values.
   When a message is received, the server immediately updates the string of LEDs using a WS281X library.
   The library can be found here: https://github.com/jgarff/rpi_ws281x
   The HTTP server (server.py) was based on one of the examples included in this package.

2. A live video stream encoder.
   A fork of mjpg-streamer with support for the raspicam was used.
   https://github.com/jacksonliam/mjpg-streamer
   This provides low-latency (but high-bandwidth) video that can be displayed in most browsers without any complicated plugins.
   This works very well on local connections (i.e. LANs)

3. A tool to generate a mapping between an on-screen pixel and an LED.
   This is the 'magic' part.
   When the string of LEDs is draped over a tree, the position of each LED is essentially random - i.e. the co-ordinates of each LED in 3D-space cannot easily be controlled.
   However, from the view point of a camera pointed at the LEDs, the position of each LED can be mapped to a 2D coordinate as follows:
   * In a dark room, the first LED in the string is illuminated
   * A still picture taken from the camera
   * The picture is analysed to find the brightest pixel
   * The co-ordinates of this pixel are the apparent co-ordinates of the LED
   The process is repeated for each LED in the string, and in this way a map between the LED index (i.e. the number of the LED in the string) and the apparent pixel co-ordinates (as viewed from the camera location) is built up.
   As long as the LEDs and camera remain in fixed positions, the co-ordinates will be correct.

4. A webpage displating the live video, with Javascript to control the HTTP Server.
   The video stream is displayed behind a transparent DIV.
   A colour-chooser widget is presented to allow the 'brush' colour to be set (RBG value),
   When a click (or touch) is detected on the DIV, the co-ordinates are taken from the event. 
   Using the map created in (3), any pixel nearby - i.e. within a 'brush radius' of the event co-ordinates - is marked with the selected RGB value.
   An array of all pixels is then sent to the server in (1).

  
# How to build

## Hardware
You'll need some strings of WS2812 (or WS2811) LEDs. The more the merrier!
The strings are often sold in chains of 50, but can be daisy-chained together.

Here is an example listing on Amazon, bear in mind there are many different sources for these parts:
https://www.amazon.co.uk/WS2811-Pixels-digital-Addressable-String/dp/B00MXW054Y

When starting off, a single string of LEDs can be powered from a small-ish 5V power supply.
However, once you have several strings connected together, the power requirements become substatial.
At full brightness (white), each LED is likely to draw about 60mA. Thus, a string of 50 LEDs can draw up to 3A, and eight strings daisy-chained together could draw 24!

The wire used in the strings is not thick enough for this kind of current.
If voltage is applied to only one end of a long string, the voltage drop along the wire will cause inconsistencies in colour, and will prevent the LEDs further down the chain from lighting at all.
To power long strings, either several independant power supplies must be used, or substantial cables must be used to distribute the 5V all the way along

![Wiring diagram](https://raw.githubusercontent.com/leocurrie/xmastree-painting/master/images/wiring.png "Wiring diagram")

## Software

1. Get the ws281x library running and working with your hardware - download and follow the instructions here:
   https://github.com/jgarff/rpi_ws281x

2. Once you are able to run the example scripts from the ws281x driver, run server.py
   Test that it is working using this curl command:
   ```
   curl -H "Content-Type: application/json" -X POST -d '{"paint": [{"p":0,"r":255,"g":255,"b":255}]}' http://127.0.0.1:8080/pixels
   ```
   If the server is running, you should see the first LED on the chain turn white

3. Get your video stream working. I used mjpg-streamer.
   https://github.com/jacksonliam/mjpg-streamer
   If you're running mjpg-streamer on the same Raspberry-Pi as the pixel server, you'll need to change which port it listens on (I used 8090).
   Once you have mjpg-streamer up and running, point your camera at your string of LED's and make sure you can get a freeze-frame from this URL:
   http://127.0.0.1:8090/?action=snapshot

4. Now the fun part. Turn the lights out.
   With the pixel server running, launch the 'calibrate.py' script, and pipe the output to a file "pixels.js"
   If everything is setup correctly, you should see each LED in the chain being turned on, then off in sequence.
   Once all LEDs have been measured, the output from the script should be an array of co-ordinates.
   Copy this file into the 'static' folder.

5. Edit the file static/index.html to replace 'pi.ip.address' with the ip address of your pi / camera
   Make sure mjpg-streamer is still running, and that the pixel server is running.
   That's it. You should now be able to open the index page http://pi.ip.address:8080/static/index.html
   
  