#include <Servo.h>

#define SERVO_PAPER_PIN 3

Servo servoPaper;

void setup() {
  servoPaper.attach(SERVO_PAPER_PIN);
  // Move servo to 0° first (open)
  servoPaper.write(0);
  delay(2000);  // wait 2 seconds so you can see it move

  // Move servo to 180° (close)
  servoPaper.write(180);
}

void loop() {
  // Do nothing here
}
