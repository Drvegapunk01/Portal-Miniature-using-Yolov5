#include <Servo.h>


// variable lableling
const int LED = 13;
Servo servo;
String data;
void setup() {
  // put your setup code here, to run once:
 servo.attach(3); 
Serial.begin(9600);
pinMode(LED,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()){
  data = Serial.readStringUntil('\n');

  }
      if(data == "open_gate"){
        servo.write(90);
        // delay(1000);
      }
  else
  {
    servo.write(0);
}
}


