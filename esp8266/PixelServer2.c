#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NeoPixelBus.h>
#include <NeoPixelAnimator.h>


// Config - change these values to suit
const uint16_t PixelCount = 400; // how many LEDs you have
char ssid[] = "SKY12345"; // your wifi name
char pass[] = "ABC123"; // your wifi password

NeoGamma<NeoGammaTableMethod> colorGamma; 
NeoPixelBus<NeoRgbFeature, Neo800KbpsMethod> strip(PixelCount);
unsigned int localPort = 2390;
const int NTP_PACKET_SIZE = PixelCount * 3;
byte packetBuffer[ NTP_PACKET_SIZE];
WiFiUDP udp;


void setAllPixels(RgbColor c) {
  for (int i=0; i<PixelCount; i++) {
    strip.SetPixelColor(i,colorGamma.Correct(c));
  }
  strip.Show();
}


void setup() {
  strip.Begin();
  strip.Show();
  setAllPixels(RgbColor(255,0,0)); // set all pixels RED on startup
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  setAllPixels(RgbColor(0,255,0)); // set all pixels GREEN once associated with WiFi
  delay(1000);
  setAllPixels(RgbColor(0,0,0));
  udp.begin(localPort);
}

void loop() {
  int cb = udp.parsePacket();
  if (cb) {
    udp.read(packetBuffer, NTP_PACKET_SIZE);
    for (int i=0; i<PixelCount; i++) {
      int p = i*3;
      strip.SetPixelColor(i,colorGamma.Correct(RgbColor(packetBuffer[p], packetBuffer[p+1], packetBuffer[p+2])));
    }
    strip.Show();
  }
}
