from djitellopy import Tello
import time

# Create a Tello object
tello = Tello()

# Connect to the Tello drone
tello.connect()

# Print the battery level
print(f"Battery: {tello.get_battery()}%")

# Take off
tello.takeoff()
time.sleep(2)  # Wait for the drone to stabilize

# Fly forward for 100 cm
tello.move_forward(100)
time.sleep(2)

# Rotate clockwise by 90 degrees
tello.rotate_clockwise(90)
time.sleep(2)

# Land the drone
tello.land()

# Disconnect from the drone
tello.end()
