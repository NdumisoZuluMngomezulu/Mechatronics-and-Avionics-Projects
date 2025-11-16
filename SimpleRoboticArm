#include <Servo.h> // Include the Servo library

// Create Servo objects for each joint
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;
Servo gripperServo;

void setup() {
  // Attach the servos to their respective pins
  shoulderServo.attach(9); // Example pin 9
  elbowServo.attach(10); // Example pin 10
  wristServo.attach(11); // Example pin 11
  gripperServo.attach(12); // Example pin 12

  // Set initial positions (optional)
  shoulderServo.write(90); // 90 degrees
  elbowServo.write(90);
  wristServo.write(90);
  gripperServo.write(0); // Gripper open
}

void loop() {
  // Example: Move the shoulder servo
  for (int pos = 0; pos <= 180; pos += 1) { // Go from 0 to 180 degrees
    shoulderServo.write(pos);
    delay(15); // Wait for the servo to move
  }
  for (int pos = 180; pos >= 0; pos -= 1) { // Go from 180 to 0 degrees
    shoulderServo.write(pos);
    delay(15);
  }

  // Example: Open and close the gripper
  gripperServo.write(90); // Close gripper
  delay(1000);
  gripperServo.write(0); // Open gripper
  delay(1000);
}
