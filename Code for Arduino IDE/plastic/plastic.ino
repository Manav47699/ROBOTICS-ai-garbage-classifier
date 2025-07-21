#include <Servo.h>

// Define servo pins
#define SERVO_PAPER_PIN 3
#define SERVO_PLASTIC_PIN 6

Servo servoPaper;
Servo servoPlastic;

String input = "";

void setup() {
  Serial.begin(9600);  // Start serial communication

  // Attach servos to pins
  servoPaper.attach(SERVO_PAPER_PIN);
  servoPlastic.attach(SERVO_PLASTIC_PIN);

  // Start with both servos closed (0 degrees)
  servoPaper.write(0);
  servoPlastic.write(0);
}

void loop() {
  // If data received from Python
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');  // Read input till newline
    input.trim();  // Remove extra spaces or newline

    if (input == "paper") {
      Serial.println("Opening paper bin...");
      servoPaper.write(180);   // Open paper bin
      delay(5000);             // Wait 5 seconds
      servoPaper.write(0);     // Close paper bin
      Serial.println("Paper bin closed.");
    }
    else if (input == "plastic") {
      Serial.println("Opening plastic bin...");
      servoPlastic.write(180);  // Open plastic bin
      delay(5000);              // Wait 5 seconds
      servoPlastic.write(0);    // Close plastic bin
      Serial.println("Plastic bin closed.");
    }
    else {
      Serial.println("Unknown command.");
    }
  }
}
