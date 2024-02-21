import cv2 
from hand_tracking import HandDetector 

def calibrate_distances():
    """
    This function is used to calibrate the distances between the pointer and middle figure to set a 
    threshold for servo control. It will launch the webcam and display the video feed. The user will
    be prompted to place their RIGHT hand in front of the camera and move their fingers to the minimum distance.
    200 frames will be captured and the average distance will be calculated. The user will then be prompted
    to move their fingers to the maximum distance and the same process will be repeated. 
    
    - return: {"min": min_avg, "max": max_avg}
    """
    cap = cv2.VideoCapture(0)
    detector = HandDetector(staticMode=False, maxHands=1, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    CONFIRMATION_LENGTH = 200
    min_distance = []
    max_distance = []
    min_avg = 0
    max_avg = 0

    while ((min_avg == 0) or (max_avg == 0)):
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=True, flipType=True)
        if hands:
            print("length of min_distance: ", len(min_distance))
            print("length of max_distance: ", len(max_distance))

            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")
            print(f'Hand type: {handType1}')

            if handType1 == "Right":
                if min_avg == 0:
                    print("Please hold minimum distance for 5 seconds: ", end=" ")

                    # Calculate distance between specific landmarks on the first hand and draw it on the image
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                                scale=10)
                    print(f'Length = {length}', end=" ")
                    min_distance.append(length)
                    if len(min_distance) >= CONFIRMATION_LENGTH:
                        min_avg = sum(min_distance) / len(min_distance)
                        print(f'Average min distance = {min_avg}')

                if (max_avg == 0) and (min_avg != 0):
                    print("Please hold maximum distance for 5 seconds: ", end=" ")

                    # Calculate distance between specific landmarks on the first hand and draw it on the image
                    length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                                scale=10)
                    print(f'Length = {length}', end=" ")
                    max_distance.append(length)
                    if len(max_distance) >= CONFIRMATION_LENGTH:
                        max_avg = sum(max_distance) / len(max_distance)
                        print(f'Average max distance = {max_avg}')

        # Display the image in a window
        cv2.imshow("Image", img)

        # Keep the window open and update it for each frame; wait for 1 millisecond between frames
        cv2.waitKey(1)
    return {"min": min_avg, "max": max_avg}

def main():
    # Initialize the webcam to capture video
    # The '2' indicates the third camera connected to your computer; '0' would usually refer to the built-in camera
    cap = cv2.VideoCapture(0)

    # Initialize the HandDetector class with the given parameters
    detector = HandDetector(staticMode=False, maxHands=2, modelComplexity=1, detectionCon=0.5, minTrackCon=0.5)

    # Continuously get frames from the webcam
    while True:
        # Capture each frame from the webcam
        # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
        success, img = cap.read()

        # Find hands in the current frame
        # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
        # The 'flipType' parameter flips the image, making it easier for some detections
        hands, img = detector.findHands(img, draw=True, flipType=True)

        # Check if any hands are detected
        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            if handType1 == "Left":
                # Print the type of the first hand
                print("Left: ", end=" ")

                # Count the number of fingers up for the left hand
                fingers1 = detector.fingersUp(hand1)
                print(fingers1, end=" ") # Print the list of fingers that are up [thumb, index, middle, ring, pinky] (1 for up, 0 for down)
                print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

                # Calculate distance between specific landmarks on the first hand and draw it on the image
                length, info, img = detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                            scale=10)
                print(f'Length = {length}', end=" ")
                

            # Check if a second hand is detected
            if len(hands) == 2:
                # Information for the second hand
                hand2 = hands[1]
                lmList2 = hand2["lmList"]
                bbox2 = hand2["bbox"]
                center2 = hand2['center']
                handType2 = hand2["type"]

                # Count the number of fingers up for the second hand
                fingers2 = detector.fingersUp(hand2)
                print(f'H2 = {fingers2.count(1)}', end=" ")

                # Calculate distance between the index fingers of both hands and draw it on the image
                # landmark list: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#models
                length, info, img = detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
                                                            scale=10)

            print(" ")  # New line for better readability of the printed output

        # Display the image in a window
        cv2.imshow("Image", img)

        # Keep the window open and update it for each frame; wait for 1 millisecond between frames
        cv2.waitKey(1)

if __name__ == "__main__":
    # main()
    print("Calibrating distances... Use Right hand to calibrate.")
    print(calibrate_distances())
