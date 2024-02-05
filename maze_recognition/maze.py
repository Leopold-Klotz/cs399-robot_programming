"""
Load in a png file of a maze and create a map object with it. The map object needs to include the proper boundaries to represent the maze.
Mazes are currently 4x4 and generated with https://www.mazegenerator.net/. 
maze files:
- random_maze1.png (4x4 maze)
- random_maze2.png (4x4 maze)
- random_maze3.png (4x4 maze)
"""

import cv2
from map import Map

# Load the image
maze_image = cv2.imread('random_maze1.png')

