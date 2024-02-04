import json

class Map:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.saved_positions = {}

    def load_saved_positions(self, filepath):
        with open(filepath, 'r') as file:
            self.saved_positions = json.load(file)

    def save_saved_positions(self, filepath):
        with open(filepath, 'w') as file:
            json.dump(self.saved_positions, file)

    def navigate(self, start, end):
        # Implement your navigation logic here
        pass

    def create_path(self, start, end):
        # Implement your path creation logic here
        pass

    def display_map(self):
        for row in self.grid:
            print(' '.join(str(cell) for cell in row))

    def display_saved_positions(self):
        for position, label in self.saved_positions.items():
            print(f"{label}: {position}")

if __name__ == "__main__":
    map = Map()
    map.display_map()
