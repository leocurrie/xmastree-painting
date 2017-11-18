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



## Software

1. Get the ws281x library running and working with your hardware

https://github.com/jgarff/rpi_ws281x
