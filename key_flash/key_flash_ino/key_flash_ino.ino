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

String msg;

void loop() {
  if(Serial.available() > 0){
    char data = Serial.read();
    msg += data;

    if (data == '?'){
      parseMsg(msg);
      msg = "";
    }
  }
}

void parseMsg(String data_frame){
  String R;
  String G;
  String B;
  
  R = data_frame.substring(0,2);
  G = data_frame.substring(3,5);
  B = data_frame.substring(6,8);
  
  if (data_frame.length() < 11) {
    for (int j=0; j<strip.numPixels(); j++){
       strip.setPixelColor(j, strip.Color(R.toInt(),G.toInt(),B.toInt()));
    }
  }
  
  else {
    for (int k=9; k<41; k++) {
      if (data_frame[k] == '1') {
        strip.setPixelColor(k-9, strip.Color(R.toInt(),G.toInt(),B.toInt()));
      }
    }
  }
  strip.show();
}
