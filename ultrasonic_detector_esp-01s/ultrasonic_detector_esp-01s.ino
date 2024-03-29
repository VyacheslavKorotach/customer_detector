/*
 * HCSR04Ultrasonic/examples/UltrasonicDemo/UltrasonicDemo.pde
 *
 * SVN Keywords
 * ----------------------------------
 * $Author: cnobile $
 * $Date: 2011-09-17 02:43:12 -0400 (Sat, 17 Sep 2011) $
 * $Revision: 29 $
 * ----------------------------------
 */

#include <Ultrasonic.h>

#define TRIGGER_PIN  0
#define ECHO_PIN     2

Ultrasonic ultrasonic(TRIGGER_PIN, ECHO_PIN);
bool obstacles = false;

void setup()
  {
  Serial.begin(9600);
//  pinMode(BUZZER_PIN, OUTPUT);
  }

void loop()
  {
  float cmMsec, inMsec;
  long microsec = ultrasonic.timing();

  cmMsec = ultrasonic.convert(microsec, Ultrasonic::CM);
  inMsec = ultrasonic.convert(microsec, Ultrasonic::IN);
  Serial.print("MS: ");
  Serial.print(microsec);
  Serial.print(", CM: ");
  Serial.print(cmMsec);
  Serial.print(", IN: ");
  Serial.println(inMsec);
  if (cmMsec > 50) {
    obstacles = false;
  }
  else {
    obstacles = true;
  }
//  digitalWrite(BUZZER_PIN, !(obstacles));
  Serial.println("Obstacles = " + String(obstacles));
  delay(500);
  }
