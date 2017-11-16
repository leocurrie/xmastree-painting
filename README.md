# xmastree-painting
The idea behind the tree lights is that a user can 'paint' colour onto a christmas tree in the same way that you can paint on a computer screen.
The project is made from several different software and hardware components.

## Hardware

Hardware wise, the project was implemented with several strings of WS2812 LEDs. These are commonly sold in strings of 50.
The strings were daisy-chained together, with appropriate power supply arrangements. The data input to the string was fed directly from a Raspberry Pi.
Although the specs say that the WS2812 requires a 5V signal, the 3.3v signal from the RPi seemed to work fine.
The video camera used was a Raspberry Pi camera.

The project could certainly be implemented with different hardware - for example, most modern USB webcams are able to deliver MJPG streams and thus could be used in place of the Raspberry Pi webcam.
An Arduino, or even an ESP8266 module could be used to implement the server.

## Software

There are 4 main components

1. An HTTP server wrto control a string of WS2811/WS2812 LEDs
   The HTTP server handles JSON messages posted from the UI. These messages simply contain an array of pixel colours, there is one array element for each LED in the string. The pixel colours are passed as RGB values.
   When a message is received, the server immediately updates the string of LEDs using a WS281X library.
   The library can be found here: https://github.com/jgarff/rpi_ws281x
   The HTTP server (server.py) was based on one of the examples included in this package.

2. A live video stream encoder
   A fork of mjpg-streamer with support for the raspicam was used.
   https://github.com/jacksonliam/mjpg-streamer
   This provides low-latency (but high-bandwidth) video that can be displayed in most browsers without any complicated plugins.
   This works very well on local connections (i.e. LANs)

3. A tool to generate a mapping between an on-screen pixel and an LED
   This is the 'magic' part.
   When the string of LEDs is draped over a tree, the position of each LED is essentially random - i.e. the co-ordinates of each LED in 3D-space cannot easily be controlled.
   However, from the view point of a camera pointed at the LEDs, the position of each LED can be mapped to a 2D coordinate as follows:
   * In a dark room, the first LED in the string is illuminated
   * A still picture taken from the camera
   * The picture is analysed to find the brightest pixel
   * The co-ordinates of this pixel are the apparent co-ordinates of the LED
   The process is repeated for each LED in the string, and in this way a map between the LED index (i.e. the number of the LED in the string) and the apparent pixel co-ordinates (as viewed from the camera location) is built up.
   As long as the LEDs and camera remain in fixed positions, the co-ordinates will be correct.

4. A webpage displating the live video, with Javascript to control the HTTP API
   The video stream is displayed behind a transparent DIV.
   A colour-chooser widget is presented to allow the 'brush' colour to be set (RBG value),
   When a click (or touch) is detected on the DIV, the co-ordinates are taken from the event. 
   Using the map created in (3), any pixel nearby - i.e. within a 'brush radius' of the event co-ordinates - is marked with the selected RGB value.
   An array of all pixels is then sent to the server in (1).
