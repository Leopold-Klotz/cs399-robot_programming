from robotArm import RobotArm
import time
import threading

# Sequence to grab the ball from the designated ball spot
def grabBall(arm):
    speech_thread = threading.Thread(target=arm.speak, args=("I am grabbing the ball",))
    # home arm
    print("Homing arm...")
    arm.home_arm()

    speech_thread.start() # start speaking
    # move arm to ball spot
    print("Moving arm to ball spot...")
    arm.loadPositionSettings("ballSquare")
    # open claw
    print("Opening claw...")
    arm.setClaw(1100, wait=False)
    # close claw
    print("Closing claw...")
    arm.setClaw(2250, wait=False)

    # transport ball
    print("Transporting ball...")
    arm.loadPositionSettings("ballTransport")
    time.sleep(1)
    # place ball
    print("Placing ball...")
    arm.loadPositionSettings("ballPlace")
    time.sleep(1)

    # open claw
    print("Opening claw...")
    arm.setClaw(1200, wait=False)

    speech_thread.join() # wait for the speaking to finish

def kickBall(arm):
    speech_thread = threading.Thread(target=arm.speak, args=("I will take a free kick!",))
    # home arm
    print("Homing arm...")
    arm.home_arm()

    speech_thread.start() # start speaking

    # prep the kick
    print("moving to pre-kick position...")
    arm.loadPositionSettings("prepKick")
    time.sleep(2)

    # close claw
    print("Closing claw...")
    arm.setClaw(2300, wait=False)

    # swift kick
    print("Swift kick!")
    arm.setPosition(3, 1500, duration = 500, wait=False)

    speech_thread.join() # wait for the speaking to finish

# Emote to the user that the robot is happy
def celebrate(arm):
    speech_thread = threading.Thread(target=arm.speak, args=("I scored!",))
    # home arm
    print("Homing arm...")
    arm.home_arm()

    speech_thread.start() # start speaking

    # celebrate
    print("Celebrating!")
    for _ in range(2):
        arm.setArt1(500, wait=False)
        arm.setArt5(500, wait=False)
        arm.setPosition([[5, 2000], [4, 2500], [3, 1000]], wait=False)
        time.sleep(1)
        arm.setArt1(2500, wait=False)
        arm.setArt5(2500, wait=False)
        arm.setPosition([[5, 1500], [4, 1500], [3, 1500]], wait=False)

    speech_thread.join() # wait for the speaking to finish
    arm.home_arm()

def main():
    port = "USB"  # Replace with the correct port
    arm = RobotArm(port)

    # arm.wave()
    time.sleep(1)
    arm.speak("Today I will be playing soccer!")
    print("Grabbing ball...")
    grabBall(arm)
    time.sleep(3)
    print("Kicking ball...")
    kickBall(arm)
    arm.speak("Did I score?")
    score = input("Did I score? (y/n): ")
    if score == "y":
        arm.speak("I scored!")
        celebrate(arm)
    else:
        arm.speak("That's okay, maybe by the end of the term I will be able to score.")

if __name__ == "__main__":
    main()

