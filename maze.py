from robotArm import RobotArm
import time
import threading

def navigateMaze(arm, positions):
    #home arm
    print("Homing arm...")
    arm.home_arm()

    for position in positions:
        # move arm to position
        print("Moving arm to position " + position + "...")
        arm.loadPositionSettings(position)

        time.sleep(1) # pause for a second before going to the next position


def main():
    port = "USB"  # Replace with the correct port
    arm = RobotArm(port)

    # arm.wave()
    time.sleep(1)

    positions = ["sq1", "sq2", "sq6", "sq7", "sq11", "sq12"]  # Replace with the positions from saved_positions.json
    navigateMaze(arm, positions)

if __name__ == "__main__":
    main()

