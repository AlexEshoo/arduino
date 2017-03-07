#include "LPD8806.h"
#include "SPI.h"

const int TRIGGER_PIN = 6;
const int TIMER_OUT_PIN = 7;
int timerState = 0;

int nLEDs = 32;
int dataPin = 2;
int clockPin = 3;

int i;

LPD8806 strip = LPD8806(nLEDs,dataPin,clockPin);

void setup() {
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(TIMER_OUT_PIN, INPUT);
  pinMode(13, OUTPUT);
  digitalWrite(TRIGGER_PIN, HIGH);
  
  strip.begin();
  strip.show();
  
  Serial.begin(115200);
}

String msg;

void loop() {
  timerState = digitalRead(TIMER_OUT_PIN);
  if (timerState == LOW) {
    rainbowIdle();
  }
  
  else if(Serial.available() > 0){
    triggerTimer();
    char data = Serial.read();
    msg += data;

    if (data == '?'){
      parseMsg(msg);
      msg = "";
    }
  }
} 

void triggerTimer() {
  digitalWrite(TRIGGER_PIN, LOW);
  //delay(5);
  /* When included, triggering works as desired
  (resets on new message, idle 27s out from last press)
  but input delay is large.
  When left out, reset is not a sure thing, but serial 
  data always recieved.*/
  digitalWrite(TRIGGER_PIN, HIGH);
  return;
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

void rainbowIdle() {
  int i, j;
   
  for (j=0; j < 384; j++) {     // 3 cycles of all 384 colors in the wheel
    for (i=0; i < strip.numPixels(); i++) {
      if (Serial.available() > 0) {
        triggerTimer();
        return;
      }
      strip.setPixelColor(i, Wheel( (i + j) % 384));
    }  
    strip.show();   // write all the pixels out
    delay(100);
  }
}

//Input a value 0 to 384 to get a color value.
//The colours are a transition r - g -b - back to r
uint32_t Wheel(uint16_t WheelPos)
{
  byte r, g, b;
  switch(WheelPos / 128)
  {
    case 0:
      r = 127 - WheelPos % 128;   //Red down
      g = WheelPos % 128;      // Green up
      b = 0;                  //blue off
      break; 
    case 1:
      g = 127 - WheelPos % 128;  //green down
      b = WheelPos % 128;      //blue up
      r = 0;                  //red off
      break; 
    case 2:
      b = 127 - WheelPos % 128;  //blue down 
      r = WheelPos % 128;      //red up
      g = 0;                  //green off
      break; 
  }
  return(strip.Color(r,g,b));
}
