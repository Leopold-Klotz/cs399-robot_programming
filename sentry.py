# This file will allow the user to play a game of simon says with the robot arm

import time
import random
from robotArm import RobotArm
from hand_recognition.finger_tracking import calibrate_distances, recognize_digit
import cv2
from hand_recognition.hand_tracking import HandDetector
from pickAndPlace.blob import blob_detect, draw_window, draw_keypoints

MISTAKE_THRESHOLD = 0.2
HANDTRACKING_LIMIT = 45 # 45 seconds of hand control
CONTROL_LANDMARKS = [8, 4]  # landmarks for the tip of the pointer and thumb (change to thumb?)
COMMAND_HOLD_MS = 5
ROTATION_STEP = 2

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
        # adjust the grab positions to the current art 1 position
        self.arm.adjust_saved_position("grab_open", 1, self.arm.getArticulation(1))
        self.arm.adjust_saved_position("grab_closed", 1, self.arm.getArticulation(1))

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

        ## parameters for blob detection
        target_location = {"x": 400, "y": 380, "radius": 60}

        #--- Define HSV limits
        blue_min = (22,79,127)
        blue_max = (169, 255, 255) 
        
        #--- Define area limit [x_min, y_min, x_max, y_max] adimensional (0.0 to 1.0) starting from top left corner
        window = [0.05, 0.25, 0.95, 0.95]
        
        blob_parameters = cv2.SimpleBlobDetector_Params()
        blob_parameters.filterByArea = False
        blob_parameters.minArea = 100
        blob_parameters.maxArea = 1000
        blob_parameters.filterByCircularity = True
        blob_parameters.minCircularity = 0.5
        blob_parameters.maxCircularity = 1.0
        blob_parameters.filterByConvexity = True
        blob_parameters.minConvexity = 0.5
        blob_parameters.filterByInertia = True
        blob_parameters.minInertiaRatio = 0.25
        ## end parameters for blob detection

        # keep looking for image
        cap = cv2.VideoCapture(0)

        # send arm to monitoring position
        self.arm.loadPositionSettings("sentry_monitor")

        # time the object is in the inbound region
        inbound_time = 0

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

            frame = resized_frame

            ## blob detection
            #-- Detect keypoints
            keypoints, _ = blob_detect(frame, blue_min, blue_max, blur=10, 
                                        blob_params=blob_parameters, search_window=window, imshow=False)
            #-- Draw search window
            frame     = draw_window(frame, window)

            #-- click ENTER on the image window to proceed
            draw_keypoints(frame, keypoints, imshow=False)

            if keypoints:
                # Display the keypoint coordinates on top of the image
                x, y = keypoints[0].pt
                x = int(x)
                y = int(y)
                print("keypoint coordinates: ", (x,y), end='\r')
                print(" ")
                cv2.putText(frame, f"Keypoint: ({x}, {y})", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 225), -1)

                distance_to_target = ((x - target_location["x"])**2 + (y - target_location["y"])**2)**0.5 # **0.5 is the same as sqrt
            ## end blob detection
                
            # adjust base towards the object
            if keypoints:
                # if the keypoint is to the left of the target, step the base to the left, and vice versa
                if x < target_location["x"]:
                    # display left facing arrow
                    arrow = "<--"
                    cv2.putText(frame, arrow, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_artOne = self.arm.getArticulation(1)
                    self.arm.setArticulation(1, current_artOne + ROTATION_STEP)
                elif x > target_location["x"]:
                    # display right facing arrow
                    arrow = "-->"
                    cv2.putText(frame, arrow, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    current_artOne = self.arm.getArticulation(1)
                    self.arm.setArticulation(1, current_artOne - ROTATION_STEP)

            print(" ")  # New line for better readability of the printed output

            # draw target circle
            if keypoints:
                if (x - target_location["x"])**2 + (y - target_location["y"])**2 < target_location["radius"]**2:
                    cv2.circle(frame, (target_location["x"], target_location["y"]), target_location["radius"], (0, 255, 0), 5)
                    cv2.putText(frame, f"Inbound Time: {int(inbound_time/2.5)}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print(f"Inbound Time: {int(inbound_time)}")
                    inbound_time += 1
                else:
                    cv2.circle(frame, (target_location["x"], target_location["y"]), target_location["radius"], (0, 0, 255), 5)
                    inbound_time = 0

            cv2.imshow('Live', frame)

            key = cv2.waitKey(1)

            if inbound_time > COMMAND_HOLD_MS * 2.5: # 5 seconds -> command hold time from ms to s
                # pick up the object
                print("grabbing object")
                self.grab_object()
                print("object grabbed")

                inbound_time = 0

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
