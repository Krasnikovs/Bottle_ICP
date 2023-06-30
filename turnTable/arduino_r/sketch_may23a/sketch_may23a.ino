#include <Stepper.h>
#include <math.h>
#include <stdlib.h>

#define STEPS 2048

Stepper stepper(STEPS, 8, 10, 9, 11);

void setup() {

  Serial.begin(9600);

}

void loop() {

  if (Serial.available() > 0) {
    int degres = Serial.parseInt();
    float dtosteps = 2048.0/360.0;
    int turnBy = dtosteps*degres;
    stepper.setSpeed(5);
    stepper.step(turnBy);
    
    Serial.println("Turn complete");
  }
  
}
