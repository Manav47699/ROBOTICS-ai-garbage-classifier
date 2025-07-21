#include <Servo.h>

// Servo pins
#define SERVO_PAPER_PIN 3
#define SERVO_PLASTIC_PIN 6

// IR sensor pin (shared for both bins)
#define IR_SENSOR_PIN 8

Servo servoPaper;
Servo servoPlastic;

String input = "";

void setup() {
  Serial.begin(9600);

  // IR sensor
  pinMode(IR_SENSOR_PIN, INPUT);

  // Attach servos
  servoPaper.attach(SERVO_PAPER_PIN);
  servoPlastic.attach(SERVO_PLASTIC_PIN);

  // Close both bins
  servoPaper.write(180);
  servoPlastic.write(180);

  Serial.println("System ready. Waiting for input...");
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();

    Serial.print("Received: ");
    Serial.println(input);

    if (input == "plastic") {
      Serial.println("Opening plastic bin...");
      servoPlastic.write(0);

      waitForIRDrop();
      
      servoPlastic.write(180);
      Serial.println("Plastic bin closed.");
    }

    else if (input == "paper") {
      Serial.println("Opening paper bin...");
      servoPaper.write(0);

      waitForIRDrop();
      
      servoPaper.write(180);
      Serial.println("Paper bin closed.");
    }

    else {
      Serial.println("Unknown input.");
    }
  }
}

// Wait until IR sensor detects object (i.e., LOW signal)
void waitForIRDrop() {
  Serial.println("Waiting for object to drop...");
  unsigned long start = millis();
  while (digitalRead(IR_SENSOR_PIN) == HIGH) {
    if (millis() - start > 5000) {
      Serial.println("Timeout waiting for object.");
      break;
    }
  }
  Serial.println("Object detected by IR sensor.");
  delay(500); // Small delay before closing
}
