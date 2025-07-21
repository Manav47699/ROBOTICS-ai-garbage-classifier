#include <Servo.h>

#define SERVO_PAPER_PIN 3
#define SERVO_PLASTIC_PIN 6

Servo servoPaper;
Servo servoPlastic;

String input = "";

void setup() {
  Serial.begin(9600);
  
  servoPaper.attach(SERVO_PAPER_PIN);
  servoPlastic.attach(SERVO_PLASTIC_PIN);

  // Start closed (reversed direction)
  servoPaper.write(180);
  servoPlastic.write(180);

  Serial.println("Arduino Ready");
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();  // remove extra whitespace

    if (input == "paper") {
      Serial.println("Opening Paper Bin");
      servoPaper.write(0);    // Open
      delay(3000);            // Keep open for 3s
      servoPaper.write(180);  // Close
    }
    else if (input == "plastic") {
      Serial.println("Opening Plastic Bin");
      servoPlastic.write(0);   // Open
      delay(3000);             // Keep open for 3s
      servoPlastic.write(180); // Close
    }
  }
}
