// Define Motor Driver Pins (Example uses an L298N driver)
const int motorLeftEnable = 5;
const int motorLeftDir1 = 6;
const int motorLeftDir2 = 7;

const int motorRightEnable = 10;
const int motorRightDir1 = 8;
const int motorRightDir2 = 9;

const int intakeMotorPin = 11; // Motor controlling the ball sweeper mechanism

void setup() {
  Serial.begin(9600);
  
  pinMode(motorLeftEnable, OUTPUT);
  pinMode(motorLeftDir1, OUTPUT);
  pinMode(motorLeftDir2, OUTPUT);
  
  pinMode(motorRightEnable, OUTPUT);
  pinMode(motorRightDir1, OUTPUT);
  pinMode(motorRightDir2, OUTPUT);

  pinMode(intakeMotorPin, OUTPUT);
  
  stopRobot();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    // Turn on the ball sweeper mechanism globally while hunting/collecting
    analogWrite(intakeMotorPin, 180); 

    if (command == "FORWARD") {
      moveForward();
    } else if (command == "LEFT") {
      turnLeft();
    } else if (command == "RIGHT") {
      turnRight();
    } else if (command == "COLLECT") {
      // Slow down to allow the intake sweeper to grab the ball comfortably
      moveForwardSlowly(); 
    } else if (command == "STOP") {
      stopRobot();
    }
  }
}

void moveForward() {
  analogWrite(motorLeftEnable, 200);
  analogWrite(motorRightEnable, 200);
  digitalWrite(motorLeftDir1, HIGH);
  digitalWrite(motorLeftDir2, LOW);
  digitalWrite(motorRightDir1, HIGH);
  digitalWrite(motorRightDir2, LOW);
}

void moveForwardSlowly() {
  analogWrite(motorLeftEnable, 100);
  analogWrite(motorRightEnable, 100);
  digitalWrite(motorLeftDir1, HIGH);
  digitalWrite(motorLeftDir2, LOW);
  digitalWrite(motorRightDir1, HIGH);
  digitalWrite(motorRightDir2, LOW);
}

void turnLeft() {
  analogWrite(motorLeftEnable, 150);
  analogWrite(motorRightEnable, 150);
  digitalWrite(motorLeftDir1, LOW);
  digitalWrite(motorLeftDir2, HIGH);
  digitalWrite(motorRightDir1, HIGH);
  digitalWrite(motorRightDir2, LOW);
}

void turnRight() {
  analogWrite(motorLeftEnable, 150);
  analogWrite(motorRightEnable, 150);
  digitalWrite(motorLeftDir1, HIGH);
  digitalWrite(motorLeftDir2, LOW);
  digitalWrite(motorRightDir1, LOW);
  digitalWrite(motorRightDir2, HIGH);
}

void stopRobot() {
  digitalWrite(motorLeftEnable, LOW);
  digitalWrite(motorRightEnable, LOW);
  analogWrite(intakeMotorPin, 0); // Turn off sweeper when stationary
}