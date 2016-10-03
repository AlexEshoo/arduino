#include "LPD8806.h"
#include "SPI.h"

const int button_pin = 6;
int nLEDs = 32;
int dataPin = 2;
int clockPin = 3;
int potPin = A0;

LPD8806 strip = LPD8806(nLEDs,dataPin,clockPin);

void setup() {
  strip.begin();
  strip.show();
  Serial.begin(115200);
}

void loop() {
 if(Serial.available() > 0){
   char data = Serial.read();
   for (int j=0; j<strip.numPixels(); j++){
     strip.setPixelColor(j, strip.Color(127,127,127));
   }
   strip.show();
   char str[2];
   str[0] = data;
   str[1] = '\0';
   Serial.print(str);
   for (int j=0; j<strip.numPixels(); j++){
     strip.setPixelColor(j, strip.Color(0,0,0));
   }
   strip.show()
 }
}
