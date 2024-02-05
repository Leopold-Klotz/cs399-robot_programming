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