Robot Arm Controller

Requirements:
$ pip install -r requirements.txt
- Note: the xarm package on pip is slightly different from the one used in this project. 
  The one used in this project is a modified version of the xarm package that is not 
  available on pip. The modified version is available in the xarm folder.

The robotArm controller class builds on the controller created by "ccourson" for
the xArmServoController. There is added functionality to control articulations 
instead of servos, along with a homing sequence, a waving sequence, and a function
to speak. The most significant improvement is the ability to save and load positions
for the arm from saved_positions.json. When run as a file, robotArm.py will present 
a command line interface to control the arm.

Inspiration package: https://github.com/ccourson/xArmServoController

Activating the virtual environment:
$ source venv/Scripts/activate

Running (as a file):
$ python robotArm.py


Maze Recognition

Requirements:
$ pip install -r requirements.txt
- Note: opencv for python is listed in the requirements.txt, but it is only necessary for
    the maze recognition. If you do not need maze recognition, you can remove it from the
    requirements.txt file.

The Map class stores data about a collection of Cells. A Cell contains information about the
boundaries on the top, bottom, left, and right, as well as the corresponding location in
saved_positions.json. The map object should be created, and then an image of a maze can be
passed into the .populate_map() method. This method will use the image to create a map of
the maze. The .solve_map() method can be used to solve the maze and return a list of cells
for the arm to navigate through. There are three provided images in the maze_recognition
folder that can be used as example mazes. Mazes are expected to be have the entrance on the
top, and the exit on the bottom. Only 4x4 mazes are guaranteed to work with the current
implementation.

Maze Generator: https://www.mazegenerator.net/ 

Running (as a file): 
$ cd maze_recognition
$ python map.py


Additional Files:
- saved_positions.json: A file to store the positions of the arm. The arm can be moved to a
    position and saved to this file. The arm can also be moved to a position from this file.
- basic_maze.py: A file to running the script for the week 4 assignment in CS399. The file
    traces through a drawn maze and is the precursor to the maze recognition functionality.
    https://youtu.be/qEpFSm2LwTQ 
- navigate_maze.py: A file to run the script for the week 5 assignment in CS399. The file
    uses the maze recognition functionality to take a picture of a maze and navigate through
    it.
- play_soccer.py: This file is a script which had the robot arm pick up a ball and take a free
    kick. It is the script for the week 1/2/3 assignment in CS399. 
    https://youtu.be/ym5JK1RDq7U 
- test_functions.py: A file to test the functionality of the robotArm class. This file is not
    necessary for the robotArm class to function

Simon Says:
- have the arm execute commands if simon says to do so.
- Arm will home on class initialization
- Arm executes command if simon says to do so, with a random number deciding if the arm will behave properly or not.
- commands: 
    - "quit": quits the game
    - "simon says __": simon says to do something
        - "move articulation # to position #": move the arm to a position given by the user (500-2500)
        - "say __": have the robot arm speak something
        - "wave": have the robot arm wave
        - "home arm": have the robot arm move to the home position
        - "set saved position __": load a saved position into the arm
        - "calibrate": calibrates the arm's hand tracking control
        - "hand control": control the arm with hand tracking

examples:
- "simon says move articulation one to position 750"
- "simon says say hello"
- "simon says wave"
- "simon says home arm"
- "move articulation one to position 1500"


Hand Tracking Addition:
Requirements:
- pip install openCV-python, mediapipe
hand landmarking model: https://developers.google.com/mediapipe/solutions/vision/hand_landmarker#get_started

    The program utilizes Googles mediapipe library to track the hand and control the robot arm.
    The finger regcognition was first implemented by Computer Vision Zone, but adjusted
    to suit my needs. The hand tracking is used to control the robot arm. The user can hold up their
    left hand with the articulation number they want to control, and the right hand to control the
    servo with a pinching motion. Two fists should start the hand tracking control, and two open 
    hands should stop it. There is also a timeout feature that will stop the hand tracking after 
    a certain amount of time. 

    Additionally a calibration step was added to threshold the distance between the pointer
    and thumb on the right hand. This was thresholded to the servo range of 500-2500. 
    Import functions to use hand tracking in game specific scenario.
Files: 
- hand_tracking.py: Hand detector class from Computer Vision Zone using mediapipe model.
- finger_tracking.py: Adjustments to better apply the tracking.


to connect to the robot over ssh must use x11 forwarding. use the command:
- ssh -X robot@<addr> 
- <for me> connect with: ssh robot

