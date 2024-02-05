import cv2
from map import Map

# Load the maze image
maze_image = cv2.imread('random_maze1.png')

# Convert the image to grayscale
maze_gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a binary image
_, maze_binary = cv2.threshold(maze_gray, 127, 255, cv2.THRESH_BINARY)

# Perform contour detection to find the boundaries of the maze
contours, _ = cv2.findContours(maze_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a map object
maze_map = Map()  # map object is a 4x4 grid

# Populate the map with the maze information
for row in range(4):
    for col in range(4):
        # Determine if the cell is a wall or open space based on contour detection results
        is_wall = cv2.pointPolygonTest(contours[0], (col, row), False) >= 0
        maze_map.set_cell(row, col, is_wall) 

# Find the route through the maze
route = maze_map.find_route()

# Print the route
print(route)
