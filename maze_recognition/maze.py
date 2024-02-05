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

# set the image size to be a multiple of 4
maze_image = cv2.resize(maze_image, (640, 640))

# Convert the image to grayscale
gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)

# Threshold the image
_, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)


# Divide the image into 4x4 grid
width = 4
height = 4
cell_width = thresh.shape[1] // width
cell_height = thresh.shape[0] // height

# Create a map object
maze_map = Map(width, height)

# Set the boundaries of the cells based on black pixels on the edges
for i in range(height): # Loop through the rows
    for j in range(width): # Loop through the columns
        cell = thresh[i * cell_height:(i + 1) * cell_height, j * cell_width:(j + 1) * cell_width] # cell is a 2D array of the cell's pixels

        # get a 1d array of the top row of pixels of the cell
        cell = cell.flatten()
        top_row = cell[0:cell_width]
        bottom_row = cell[-cell_width:]
        left_column = cell[0::cell_width]
        right_column = cell[cell_width - 1::cell_width]

        # Get the value which appears most in the array
        top_row = max(set(top_row), key = list(top_row).count)
        bottom_row = max(set(bottom_row), key = list(bottom_row).count)
        left_column = max(set(left_column), key = list(left_column).count)
        right_column = max(set(right_column), key = list(right_column).count)

        # Set the boundaries of the cell
        if top_row == 0:
            maze_map.grid[i][j].set_upper_boundary(True)
        else:
            maze_map.grid[i][j].set_upper_boundary(False)
        if bottom_row == 0:
            maze_map.grid[i][j].set_bottom_boundary(True)
        else:
            maze_map.grid[i][j].set_bottom_boundary(False)
        if left_column == 0:
            maze_map.grid[i][j].set_left_boundary(True)
        else:
            maze_map.grid[i][j].set_left_boundary(False)
        if right_column == 0:
            maze_map.grid[i][j].set_right_boundary(True)
        else:
            maze_map.grid[i][j].set_right_boundary(False)


# Print the map
maze_map.print_map()
