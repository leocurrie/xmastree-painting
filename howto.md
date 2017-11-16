# How to build

## Hardware
You'll need some strings of WS2812 (or WS2811) LEDs. The more the merrier!
The strings are often sold in chains of 50, but can be daisy-chained together.

Here is an example listing on Amazon, bear in mind there are many different sources for these parts:
https://www.amazon.co.uk/WS2811-Pixels-digital-Addressable-String/dp/B00MXW054Y

When starting off, a single string of LEDs can be powered from a small-ish 5V power supply.
However, once you have several strings connected together, the power requirements become substatial.
At full, white brightness, each LED is likely to draw about 60mA. Thus, a string of 50 LEDs, with all LEDs at full brightness will draw 3A
Eight strings daisy-chained together could draw 24A!

The wire used in the strings commonly available is not rated for this kind of current. 
If voltage is only applied to one end of a long string, the voltage drop in the wire will cause inconsistencies in colour, and will prevent the LEDs further down the chain from lighting at all.
Therefore, it will be necessary to feed power to the chain at each end. For example, with 3 chains connected together, power should be applied at both ends of the long chain, plus each junction.






1. Get the ws281x library running and working with your hardware

https://github.com/jgarff/rpi_ws281x
