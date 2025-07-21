#include <Servo.h>

// Paper ultrasonic
#define TRIG_PAPER 11
#define ECHO_PAPER 9

// Plastic ultrasonic
#define TRIG_PLASTIC 13
#define ECHO_PLASTIC 12

// Servo pins
#define SERVO_PAPER_PIN 3
#define SERVO_PLASTIC_PIN 6

Servo servoPaper;
Servo servoPlastic;

String input = "";

void setup() {
  Serial.begin(9600);

  // Set ultrasonic pins
  pinMode(TRIG_PAPER, OUTPUT);
  pinMode(ECHO_PAPER, INPUT);
  pinMode(TRIG_PLASTIC, OUTPUT);
  pinMode(ECHO_PLASTIC, INPUT);

  // Attach servos
  servoPaper.attach(SERVO_PAPER_PIN);
  servoPlastic.attach(SERVO_PLASTIC_PIN);

  // Start with both bins CLOSED
  servoPaper.write(180);
  servoPlastic.write(180);

  Serial.println("System ready. Waiting for input...");
}

void loop() {
  if (Serial.available()) {
    input = Serial.readStringUntil('\n');
    input.trim();  // Remove newline/whitespace

    Serial.print("Received: ");
    Serial.println(input);

    if (input == "plastic") {
      long dist = getDistance(TRIG_PLASTIC, ECHO_PLASTIC);
      Serial.print("Plastic bin distance: ");
      Serial.println(dist);

      if (dist > 10) {
        Serial.println("Opening plastic bin...");
        servoPlastic.write(0);
        delay(3000); // Keep open for 3 seconds
        servoPlastic.write(180);
        Serial.println("Plastic bin closed.");
      } else {
        Serial.println("Plastic bin is full. Not opening.");
      }
    }

    else if (input == "paper") {
      long dist = getDistance(TRIG_PAPER, ECHO_PAPER);
      Serial.print("Paper bin distance: ");
      Serial.println(dist);

      if (dist > 10) {
        Serial.println("Opening paper bin...");
        servoPaper.write(0);
        delay(3000); // Keep open for 3 seconds
        servoPaper.write(180);
        Serial.println("Paper bin closed.");
      } else {
        Serial.println("Paper bin is full. Not opening.");
      }
    }

    else {
      Serial.println("Unknown input.");
    }
  }
}

// Get distance from ultrasonic sensor
long getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 30000); // Timeout: 30ms = ~500cm
  long distance = duration * 0.034 / 2;

  if (distance == 0) return 999; // Safety fallback
  return distance;
}
