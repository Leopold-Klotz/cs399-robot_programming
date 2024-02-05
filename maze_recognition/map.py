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

    def populate_map(self, img_path):
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

    def generate_random_maze(self):
        entry_point = (random.randint(0, self.width - 1), 0)
        exit_point = (random.randint(0, self.width - 1), self.height - 1)

        stack = [entry_point]
        visited = set()

        while stack:
            current_cell = stack[-1]
            x, y = current_cell
            visited.add(current_cell)

            neighbors = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
            ]
            unvisited_neighbors = [neighbor for neighbor in neighbors if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height and neighbor not in visited]

            if unvisited_neighbors:
                next_cell = random.choice(unvisited_neighbors)
                stack.append(next_cell)

                # Remove boundary between current cell and the chosen neighbor
                if next_cell == (x - 1, y):
                    self.grid[y][x].set_left_boundary(False)
                    self.grid[next_cell[1]][next_cell[0]].set_right_boundary(False)
                elif next_cell == (x + 1, y):
                    self.grid[y][x].set_right_boundary(False)
                    self.grid[next_cell[1]][next_cell[0]].set_left_boundary(False)
                elif next_cell == (x, y - 1):
                    self.grid[y][x].set_upper_boundary(False)
                    self.grid[next_cell[1]][next_cell[0]].set_bottom_boundary(False)
                elif next_cell == (x, y + 1):
                    self.grid[y][x].set_bottom_boundary(False)
                    self.grid[next_cell[1]][next_cell[0]].set_upper_boundary(False)

                # Check if the exit point is reached
                if next_cell == exit_point:
                    break
            else:
                stack.pop()

if __name__ == "__main__":
    maze_map = Map(4, 4)

    maze_map.populate_map('random_maze1.png')
    maze_map.print_map()
