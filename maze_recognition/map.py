# Author: Leopold Klotz
# Email: klotzl@oregonstate.edu

import random
import cv2

class Cell():
    def __init__(self, u=True, b=True, l=True, r=True):
        self.upper_boundary = u
        self.bottom_boundary = b
        self.left_boundary = l
        self.right_boundary = r
        self.saved_position = None

    def set_boundaries(self, u, b, l, r):
        self.upper_boundary = u
        self.bottom_boundary = b
        self.left_boundary = l
        self.right_boundary = r

    def set_upper_boundary(self, value):
        self.upper_boundary = value

    def set_bottom_boundary(self, value):
        self.bottom_boundary = value

    def set_left_boundary(self, value):
        self.left_boundary = value

    def set_right_boundary(self, value):
        self.right_boundary = value

    def set_saved_position(self, position):
        self.saved_position = position

class Map():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.contains_maze = False
        self.solution = None
        self.assign_cell_positions()        

    def assign_cell_positions(self):
        """
        Assigns the proper string to access the cell in saved_positions.json
        """
        count = 1
        for row in self.grid:
            for cell in row:
                cell.set_saved_position("sq" + str(count))
                count += 1

    def print_map(self):
        for i, row in enumerate(self.grid):
            # Print upper boundaries
            for j, cell in enumerate(row):
                if cell.upper_boundary:
                    print("+---", end="")
                else:
                    print("+   ", end="")
            print("+")

            # Print left and right boundaries
            for j, cell in enumerate(row):
                if cell.left_boundary:
                    print("|   ", end="")
                else:
                    print("    ", end="")
            print("|")

        # Print bottom boundaries
        for j, cell in enumerate(self.grid[-1]):
            if cell.bottom_boundary:
                print("+---", end="")
            else:
                print("+   ", end="")
        print("+")

    def print_solution(self):
        if self.solution is None:
            print("No solution found")
            return
        print("Solution: ", end="")
        for i, cell in enumerate(self.solution):
            if i == len(self.solution) - 1:
                print(cell, end="")
            else:
                print(cell, end=" -> ")

    def populate_map(self, img_path):
        """
        Load in a png file of a maze and create a map object with it. The map object needs to include the proper boundaries to represent the maze.
        Mazes are currently 4x4 and generated with https://www.mazegenerator.net/. 
        There is a restriction on the maze that the entrance is always on the top and the exit is always on the bottom.
        Maze files:
        - random_maze1.png (4x4 maze)
        - random_maze2.png (4x4 maze)
        - random_maze3.png (4x4 maze)
        """
        # Load the image
        maze_image = cv2.imread(img_path)

        # set the image size to be a multiple of 4
        maze_image = cv2.resize(maze_image, (640, 640))

        # Convert the image to grayscale
        gray = cv2.cvtColor(maze_image, cv2.COLOR_BGR2GRAY)

        # Threshold the image
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Divide the image into 4x4 grid
        cell_width = thresh.shape[1] // self.width
        cell_height = thresh.shape[0] // self.height

        # Set the boundaries of the cells based on black pixels on the edges
        for i in range(self.height):  # Loop through the rows
            for j in range(self.width):  # Loop through the columns
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
                    self.grid[i][j].set_upper_boundary(True)
                else:
                    self.grid[i][j].set_upper_boundary(False)
                if bottom_row == 0:
                    self.grid[i][j].set_bottom_boundary(True)
                else:
                    self.grid[i][j].set_bottom_boundary(False)
                if left_column == 0:
                    self.grid[i][j].set_left_boundary(True)
                else:
                    self.grid[i][j].set_left_boundary(False)
                if right_column == 0:
                    self.grid[i][j].set_right_boundary(True)
                else:
                    self.grid[i][j].set_right_boundary(False)

        self.contains_maze = True

    def find_entrance(self):
        """
        Find the entrance of the maze. (The entrance is always on the top row of the maze)
        """
        if not self.contains_maze:
            print("No maze to find entrance")
            return

        for i, cell in enumerate(self.grid[0]):
            if not cell.upper_boundary:
                return 0, i  # Return coordinates of the entrance.

    def find_exit(self):
        """
        Find the exit of the maze. (The exit is always on the bottom row of the maze)
        """
        if not self.contains_maze:
            print("No maze to find exit")
            return

        for i, cell in enumerate(self.grid[-1]):
            if not cell.bottom_boundary:
                return self.height - 1, i  # Return coordinates of the exit.

    def solve_map(self):
        """
        Use a depth-first search to solve the maze.
        """
        if not self.contains_maze:
            print("No maze to solve")
            return
        print("Solving maze...")
        entrance = self.find_entrance()
        exit = self.find_exit()
        self.dfs(entrance[0], entrance[1], exit, [])
        if not self.solution:
            print("No solution found")
        else:
            print("Solution found")

    def dfs(self, row, col, exit, path):
        """
        Depth-first search algorithm to solve the maze.
        """
        if row < 0 or row >= self.height or col < 0 or col >= self.width:
            return False
        if self.grid[row][col].saved_position in path:
            return False
        if (row, col) == exit:
            path.append(self.grid[row][col].saved_position)
            self.solution = path
            return True

        path.append(self.grid[row][col].saved_position)

        if not self.grid[row][col].upper_boundary and self.dfs(row - 1, col, exit, path):
            return True

        if not self.grid[row][col].bottom_boundary and self.dfs(row + 1, col, exit, path):
            return True

        if not self.grid[row][col].left_boundary and self.dfs(row, col - 1, exit, path):
            return True

        if not self.grid[row][col].right_boundary and self.dfs(row, col + 1, exit, path):
            return True

        path.pop()
        return False

if __name__ == "__main__":
    maze_map = Map(4, 4)

    maze_map.populate_map('random_maze1.png')
    maze_map.print_map()
    maze_map.solve_map()
    maze_map.print_solution()
