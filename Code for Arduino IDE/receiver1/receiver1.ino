void setup() {
  Serial.begin(9600);  // Start serial at 9600 baud
  while (!Serial) { ; } // Wait for serial port to connect (only needed on some boards)
  Serial.println("Arduino Serial Receiver Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String incoming = Serial.readStringUntil('\n');  // Read incoming string until newline
    Serial.print("Received: ");
    Serial.println(incoming);
  }
}
