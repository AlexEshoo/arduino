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
    goIdle();
  }
  
  else if(Serial.available() > 0){
    Serial.print("Message Incoming");
    triggerTimer();
    while (Serial.available() > 0) {
      Serial.read();
    }
    Serial.print("finished reading");
    //char data = Serial.read();
    //msg += data;

    //if (data == '?'){
      //parseMsg(msg);
      //msg = "";
    //}
  }
  else {
    Serial.println(i);
    delay(1000);
    i++;
  }
} 

void triggerTimer() {
  digitalWrite(TRIGGER_PIN, LOW);
  delay(100);
  digitalWrite(TRIGGER_PIN, HIGH);
  delay(10); //Allow time for 555 out to go HIGH again
  return;
}

void goIdle() {
  i=0;
  while (Serial.available() == 0) {
    digitalWrite(13, HIGH);
    delay(100);
  }
  digitalWrite(13, LOW);
  triggerTimer();
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
