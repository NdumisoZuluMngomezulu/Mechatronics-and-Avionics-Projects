import cv2
import numpy as np
import serial
import time

# This Python script runs on the Raspberry Pi. It captures a video stream, filters for a specific color 
# (tennis ball yellow/green), calculates the horizontal error from the center of the frame, and 
# sends steering commands to the Arduino via Serial.


# Initialize Serial Communication with Arduino (Check your port via ls /dev/tty*)
try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2) # Wait for connection to stabilize
except:
    print("Arduino not connected. Running in simulation mode.")
    ser = None

# Define HSV color range for a yellow/green tennis ball
# (Adjust these values if tracking a checkered football using contours/size)
yellow_lower = np.array([29, 86, 6])
yellow_upper = np.array([64, 255, 255])

# Start video capture
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
FRAME_CENTER_X = 320

print("Ball tracking started...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Blur and convert to HSV color space
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Create a mask for yellow color
        mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        command = "STOP\n" # Default command if no ball is found

        if len(contours) > 0:
            # Find the largest contour (assumed to be the closest ball)
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)

            # Only proceed if the target is large enough to be a ball
            if radius > 10:
                # Draw visual tracking tracking markers
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 0), 2)
                
                # Calculate horizontal deviation from center
                error = int(x) - FRAME_CENTER_X

                # Simple threshold steering logic
                if error > 50:
                    command = "RIGHT\n"
                elif error < -50:
                    command = "LEFT\n"
                else:
                    command = "FORWARD\n"
                    
                # If ball is extremely close (large radius), trigger intake or stop
                if radius > 150:
                    command = "COLLECT\n"

        # Send command to Arduino
        if ser:
            ser.write(command.encode('utf-8'))
            print(f"Sent: {command.strip()} | Radius: {radius if 'radius' in locals() else 0:.1f}")

        # Display the video frame (Optional - comment out when running headless)
        cv2.imshow("Ball Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    if ser:
        ser.close()