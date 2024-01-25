from robot_intro import RobotArm
import time

def main():
    port = "USB"  # Replace with the correct port
    arm = RobotArm(port)
    # arm.wave()
    print("Grabbing ball...")
    grabBall(arm)

# Sequence to grab the ball from the designated ball spot
def grabBall(arm):
    # home arm
    print("Homing arm...")
    arm.home_arm()
    # move arm to ball spot
    print("Moving arm to ball spot...")
    arm.loadPositionSettings("ballSquare")
    # open claw
    # close claw

    # transport ball
    print("Transporting ball...")
    arm.loadPositionSettings("ballTransport")
    time.sleep(1)
    # place ball
    print("Placing ball...")
    arm.loadPositionSettings("ballPlace")
    time.sleep(1)

    # open claw

if __name__ == "__main__":
    main()

