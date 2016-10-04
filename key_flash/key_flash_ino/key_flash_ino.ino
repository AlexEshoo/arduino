#include "LPD8806.h"
#include "SPI.h"

const int button_pin = 6;
int nLEDs = 32;
int dataPin = 2;
int clockPin = 3;
int potPin = A0;

LPD8806 strip = LPD8806(nLEDs,dataPin,clockPin);

struct led {
  int R;
  int G;
  int B;
};

void setup() {
  strip.begin();
  strip.show();
  Serial.begin(115200);
}

String RGB = "000000000?";

void loop() {
 if(Serial.available() > 0){
   char data = Serial.read();
   char str[2];
   str[0] = data;
   str[1] = '\0';
   Serial.print(str);
   
   if (data == '?'){
    parseMsg(RGB);
    RGB = "";
   }
   else {
     RGB += data;
   }
//   for (int j=0; j<strip.numPixels(); j++){
//     strip.setPixelColor(j, strip.Color(127,127,127));
//   }
//   strip.show();
//   char str[2];
//   str[0] = data;
//   str[1] = '\0';
//   Serial.print(data);
//   for (int j=0; j<strip.numPixels(); j++){
//     strip.setPixelColor(j, strip.Color(0,0,0));
//   }
//   strip.show();
 }
}

void parseMsg(String data_frame){
  String R;
  String G;
  String B;
  
  R = data_frame.substring(0,2);
  G = data_frame.substring(3,5);
  B = data_frame.substring(6,8);
  
  for (int j=0; j<strip.numPixels(); j++){
     strip.setPixelColor(j, strip.Color(R.toInt(),G.toInt(),B.toInt()));
  }
  strip.show();
}
