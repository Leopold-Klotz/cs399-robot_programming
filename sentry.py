# This file will allow the user to play a game of simon says with the robot arm

import time
import random
from robotArm import RobotArm
from hand_recognition.finger_tracking import calibrate_distances, recognize_digit
import cv2
from hand_recognition.hand_tracking import HandDetector

MISTAKE_THRESHOLD = 0.2
HANDTRACKING_LIMIT = 45 # 45 seconds of hand control
CONTROL_LANDMARKS = [8, 4]  # landmarks for the tip of the pointer and thumb (change to thumb?)
COMMAND_HOLD_MS = 5

class Sentry:
    def __init__(self, port):
        try:
            self.arm = RobotArm(port)
        except:
            print("Could not connect to the robot arm. Please check the connection and try again.")
            return
        self.arm.home_arm()

        self.hand_distances = {'min': 30.305397485707655, 'max': 198.38702541542978}
        self.holding_object = False
        self.inbound_region = None

    def parse_input(self, input_string):
        # split the input into words
        words = input_string.split()

        # Remove punctuation
        words = [word.strip(",.?!") for word in words]

        # Filter out any insignificant words
        significant_words = [word for word in words if word.lower() not in ["the", "and", "or", "a", "an"]]

        return significant_words
    
    def execute_input(self, user_input):
        failed = False

        # Parse the input
        significant_words = self.parse_input(user_input)

        # if the first two words are "simon says", follow them -> random amount of mess ups
        if significant_words[:2] == ["simon", "says"]:
            if random.random() < 0.01: # chance of not executing when it should INTENTIONAL
                print("I never heard you say simon says! I'm not going to do that.")
                print("You win! I made a mistake!")
                failed = True
                return -1
            else:
                significant_words = significant_words[2:]
        else:
            if random.random() < (1 - MISTAKE_THRESHOLD): # chance of executing when it shouldn't INTENTIONAL
                print("I only do what Simon says. I'm not going to do that.")
                return
            else:
                # failed but execute action
                failed = True
                

        # Execute the command
        if "move" in significant_words:
            self.move_arm(significant_words)
        elif "say" in significant_words:
            self.say_something(significant_words)
        elif "wave" == significant_words[0]: # "Simon says wave" | "wave"
            self.arm.wave()
        elif ("home" in significant_words) and ("arm" in significant_words): # "Simon says home arm" | "home arm"
            self.arm.home_arm()
        elif ("set" in significant_words) and ("saved" in significant_words) and ("position" in significant_words):
            self.go_to_saved_position(significant_words)
        elif "calibrate" in significant_words:
            self.calibrate()
        elif "hand" in significant_words and "control" in significant_words:
            self.hand_control()
        else:
            print("I'm sorry, I don't understand that command.")

        if failed:
            print("You win! I made a mistake!")
            return -1

        return 0

    def _word_to_number(self, word):
        word_to_number_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                            "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
        return word_to_number_dict.get(word.lower())
    
    def num_to_string(self, num):
        number_to_word_dict = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
                            6: "six", 7: "seven", 8: "eight", 9: "nine", 0: "zero"}
        return number_to_word_dict.get(num)

    def move_arm(self, significant_words):
        print(significant_words)

        # find the proper articulation number
        articulation_number = significant_words[significant_words.index("articulation") + 1]
        articulation_number = self._word_to_number(articulation_number)
        
        # find the proper position number
        position_number = significant_words[significant_words.index("position") + 1]

        print("Moving arm to articulation " + str(articulation_number) + " position " + str(position_number))

        # move the arm
        self.arm.setArticulation(int(articulation_number), int(position_number))

    def say_something(self, significant_words):
        # find the proper phrase
        phrase = " ".join(significant_words[significant_words.index("say") + 1:])
        print("Speaking: " + phrase)

        # say the phrase
        self.arm.speak(phrase)

    def wave_command(self, significant_words):
        # call the wave function
        self.arm.wave()

    def go_to_saved_position(self, significant_words):
        # find the name of the saved position
        position_name = significant_words[significant_words.index("position") + 1]
        
        # go to the saved position
        self.arm.loadPositionSettings(position_name)

    def calibrate(self):
        # calibrate the distances for hand control
        print("Launching calibrating distances for hand control...")
        limits = calibrate_distances()
        print("Calibration complete!")
        print("Limits: ", limits)
        self.hand_distances = limits

    def _distance_to_position(self, live_distance, limits):
        if (self.hand_distances == None):
            print("Hand distances not calibrated. Please calibrate the hand distances first.")
            return 1500

        # return the position of the arm based on the distance
        # lower bound of position is 500, upper bound is 2500
        scaled_live_distance = (live_distance - limits["min"]) / (limits["max"] - limits["min"])
        scaled_servo_value = int(scaled_live_distance * (2500 - 500) + 500)

        # make sure the value is within the bounds
        if scaled_servo_value < 500:
            scaled_servo_value = 500
        elif scaled_servo_value > 2500:
            scaled_servo_value = 2500

        return scaled_servo_value
        
    def hand_control(self):
        """
        Function: tracks the left and right hand to send commands to the robot arm. 
        The left hand controls the articulation and the right hand controls the position.
        The user must hold both hands in a fist to activate the control and open both 
        hands to deactivate it.
        """
        start_time = time.time()
        activate = False
        continue_control = True
        articulation = []
        position = []

        cap = cv2.VideoCapture(0) 
        detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

        while continue_control and (time.time() - start_time) < HANDTRACKING_LIMIT:
            # Sensor Update
            success, img = cap.read()
            hands, img = detector.findHands(img, draw=True, flipType=True)
            if hands:
                # activate if both hands are in a fist
                if (len(hands) > 1): 
                    hand1 = hands[0]
                    hand2 = hands[1]
                    if (recognize_digit(detector.fingersUp(hand1)) == 0) and (recognize_digit(detector.fingersUp(hand2)) == 0):
                        activate = True
                        time.sleep(1) # wait for 1 second to avoid multiple activations
                if activate and (len(hands) > 1):
                    hand1 = hands[0]
                    hand2 = hands[1]
                    if hand1["type"] == "Left":
                        print("Left hand controls articulation", end=" ")
                        articulation.append(recognize_digit(detector.fingersUp(hand1))) # add to articulation avg list
                        lmList = hand2["lmList"]
                        length, info, img = detector.findDistance(lmList[CONTROL_LANDMARKS[0]][0:2], lmList[CONTROL_LANDMARKS[1]][0:2], img, color=(255, 0, 255), scale=10)
                        position.append(length) # add to position avg list
                    else:
                        print("Right hand controls position", end=" ")
                        articulation.append(recognize_digit(detector.fingersUp(hand2)))
                        lmList = hand1["lmList"]
                        length, info, img = detector.findDistance(lmList[CONTROL_LANDMARKS[0]][0:2], lmList[CONTROL_LANDMARKS[1]][0:2], img, color=(255, 0, 255), scale=10)
                        position.append(length)
                    if (recognize_digit(detector.fingersUp(hand1)) == 5) and (recognize_digit(detector.fingersUp(hand2)) == 5):
                        continue_control = False
                        activate = False

            articulation = [x for x in articulation if x != 0]
            position = [x for x in position if x != 0]
            # print("length of articulation: ", len(articulation), end=" ")
            # print("length of position: ", len(position), end="")
            # print(" ")  # New line for better readability of the printed output

            # Motion Update
            if len(articulation) >= COMMAND_HOLD_MS and len(position) >= COMMAND_HOLD_MS:
                print(" ")  # New line for better readability of the printed output
                print("Sending command to robot arm")
                print("articulation: ", articulation)
                print("position", position)
                avg_articulation = sum(articulation) / len(articulation)
                avg_position = sum(position) / len(position)
                art = round(avg_articulation)
                pos = round(self._distance_to_position(avg_position, self.hand_distances))
                print (f"Articulation: {art} Position: {pos}")
                self.arm.setArticulation(art, pos)
                articulation = []
                position = []

            # Display the image in a window
            cv2.imshow("Image", img)
            cv2.waitKey(1) # wait for 1 millisecond between frames

    def grab_object(self):
        #go to the grab position
        self.arm.loadPositionSettings("grab_open")
        time.sleep(1)
        # grab object
        self.arm.loadPositionSettings("grab_closed")
        time.sleep(1)
        # lift
        self.arm.loadPositionSettings("hold_up")
        time.sleep(1)

        self.holding_object = True

    def drop_object(self):
        # open the claw
        self.arm.setClaw(1500)
        time.sleep(1)
        self.arm.loadPositionSettings("sentry_monitor")
        time.sleep(1)

    def monitor(self):
        # looping behavior state, sentry mode or target acquired
        print("Monitor Booting...")
        time.sleep(1)

        target_lines = cv2.imread("lines_image.jpg")

        # keep looking for image
        cap = cv2.VideoCapture(0)

        # send arm to monitoring position
        self.arm.loadPositionSettings("sentry_monitor")

        print("Press Enter to grab object, 'd' to drop object, and 'q' to quit.")
        
        while True:
            ret, frame = cap.read()
            
            if not ret or frame is None:
                print("Error reading frame")
                break

            # rotate the image 90 degrees ccw
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)   
            
            # resize image
            resized_frame = cv2.resize(rotated_frame, (800, 800))

            #overlay the lines image onto the resized frame
            combined_frame = cv2.addWeighted(resized_frame, 1, target_lines, 0.5, 0)

            cv2.imshow('Live', combined_frame)

            key = cv2.waitKey(1)

            if key == 13: # ascii for enter key
                # pick up the object
                print("grabbing object")
                self.grab_object()
                print("object grabbed")

            if key == ord('d') and self.holding_object:
                # drop the object
                print("dropping object")
                self.drop_object()
                print("object dropped")

            
            if key & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

        # end
        print("...Monitor Closing")

    def monitor_distances_loop(self):
        cap = cv2.VideoCapture(0)
        detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
        while True:
            success, img = cap.read()
            hands, img = detector.findHands(img, draw=True, flipType=True)
            if hands:
                hand1 = hands[0]
                lmList1 = hand1["lmList"]
                length, info, img = detector.findDistance(lmList1[CONTROL_LANDMARKS[0]][0:2], lmList1[CONTROL_LANDMARKS[1]][0:2], img, color=(255, 0, 255), scale=10)
                # display the distance on the image

                print(f'Length = {length}, Distance = {self._distance_to_position(length, self.hand_distances)}')
            cv2.imshow("Image", img)
            cv2.waitKey(1)

    def monitor_digit_loop(self):
        cap = cv2.VideoCapture(0)
        detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)
        while True:
            success, img = cap.read()
            hands, img = detector.findHands(img, draw=True, flipType=True)
            if hands:
                hand1 = hands[0]
                fingers = recognize_digit(detector.fingersUp(hand1))
                print(f'Recognized Number = {fingers}')
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            


if __name__ == "__main__":
    sentry = Sentry("USB")
    sentry.monitor()
    # sentry.monitor_distances_loop()
    # sentry.monitor_digit_loop()