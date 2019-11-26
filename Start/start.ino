#include <AltSoftSerial.h>
AltSoftSerial BTserial; 

String c;
int val;
float current_time;
int starting;
int car_on;

void setup() {
 BTserial.begin(9600);  
 pinMode(0, OUTPUT);
 pinMode(7, OUTPUT);
 pinMode(4, INPUT_PULLUP);
 pinMode(5, OUTPUT);
 pinMode(3, OUTPUT);
 pinMode(6, OUTPUT);
 pinMode(2, OUTPUT);
 pinMode(13, OUTPUT);
 pinMode(10, INPUT_PULLUP);
 pinMode(1, INPUT);
 pinMode(11, OUTPUT);
 pinMode(12, OUTPUT);
 digitalWrite(7, HIGH);
 digitalWrite(5, HIGH);
 digitalWrite(3, HIGH);
 digitalWrite(6, HIGH);
 digitalWrite(2, HIGH);
 digitalWrite(0, LOW);
 digitalWrite(11, HIGH);
 digitalWrite(12, HIGH);
 digitalWrite(13, HIGH);
 starting = 1;
 car_on = 0;

}
void loop() {
 if (BTserial.available()){
        c = BTserial.readString();
        if (c == "passwordHere"){
          unlock();
          carOn();
        }
        if (c == "passwordHere" && car_on == 0){
          btstart();
        }
        if (c == "passwordHere"){
          unlock();
        }
        if (c == "passwordHere"){
          lock();
        }
        if (c == "passwordHere"){
          car_on = 0;
          carOff();
        }
    }
    
  if (digitalRead(10) == LOW && digitalRead(1) == HIGH){
    unlock();
    carOn();
  }
  delay(200);
  val = digitalRead(4);
  if (val == LOW){
    car_on = 0;
    carOff();
  }
}
void carOn() {
   digitalWrite(7, LOW);
   digitalWrite(3, LOW);
   digitalWrite(6, LOW);
   starting = 1;
   current_time = millis()+120000.0;
   while ((current_time - millis()) >= 0 && car_on == 0) {
      val = digitalRead(4);
      while(val == LOW){
         digitalWrite(7, HIGH);
         digitalWrite(3, HIGH);
         digitalWrite(6, HIGH);
         digitalWrite(5, LOW);
         digitalWrite(2, LOW);
         digitalWrite(13, LOW);
         starting = 0;
         val = digitalRead(4);
      }
      if (val == HIGH){
       digitalWrite(5, HIGH);
       digitalWrite(2, HIGH);
       digitalWrite(13, HIGH);
       digitalWrite(3, LOW);
       digitalWrite(7, LOW);
       digitalWrite(6, LOW);
      }
      if (starting == 0){
       current_time = -120000.0;
       car_on = 1;
      }
   }
   delay(200);
 }
 
void btstart(){
  if (car_on == 0){
   car_on = 1;
   digitalWrite(7, LOW);
   digitalWrite(3, LOW);
   digitalWrite(6, LOW);
   digitalWrite(11, LOW);
   digitalWrite(12, HIGH);
   delay(500);
   digitalWrite(11, HIGH);
   digitalWrite(12, HIGH);
   delay(500);
   digitalWrite(7, HIGH);
   digitalWrite(3, HIGH);
   digitalWrite(6, HIGH);
   digitalWrite(5, LOW);
   digitalWrite(2, LOW);
   digitalWrite(13, LOW);
   delay(1000);
   digitalWrite(5, HIGH);
   digitalWrite(2, HIGH);
   digitalWrite(13, HIGH);
   digitalWrite(3, LOW);
   digitalWrite(7, LOW);
   digitalWrite(6, LOW);
   delay(100);
   }
}

void carOff(){
   digitalWrite(5, HIGH);
   digitalWrite(2, HIGH);
   digitalWrite(13, HIGH);
   digitalWrite(3, HIGH);
   digitalWrite(7, HIGH);
   digitalWrite(6, HIGH);
   car_on = 0;
}

void lock(){
  digitalWrite(11, HIGH);
  digitalWrite(12, LOW);
  delay(500);
  digitalWrite(11, HIGH);
  digitalWrite(12, HIGH);
}

void unlock(){
  digitalWrite(11, LOW);
  digitalWrite(12, HIGH);
  delay(500);
  digitalWrite(11, HIGH);
  digitalWrite(12, HIGH);
}
