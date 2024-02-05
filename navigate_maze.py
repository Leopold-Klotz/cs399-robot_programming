from maze_recognition.map import Map
from robotArm import RobotArm
import time

def scan_new_maze():
    # Code to scan a new maze
    print("Scanning new maze...(not implemented)")
    # Add your code here
    pass

def travel_known_maze(maze_route):
    # Code to travel a known maze
    print(f"Traveling known maze: {maze_route}")
    # Add your code here

def navigateMaze(arm, positions):
    #home arm
    print("Homing arm...")
    arm.home_arm()

    for position in positions:
        # move arm to position
        print("Moving arm to position " + position + "...")
        arm.loadPositionSettings(position)

        time.sleep(1) # pause for a second before going to the next position

def main():
    port = "USB"  # Replace with the correct port
    try:
        arm = RobotArm(port)
    except:
        print("Error: Could not connect to the robot arm")
        
    map = Map(4, 4)  

    while True:
        choice = input("Enter '1' to scan a new maze or '2' to travel a known maze: ")

        if choice == '1':
            scan_new_maze()
        elif choice == '2':
            maze_choice = input("Enter the maze number (1, 2, 3, etc.): ")
            maze_choice = "maze_recognition/random_maze" + str(maze_choice) + ".png"
            map.populate_map(maze_choice)
            map.print_map()
            map.solve_map()
            path = map.solution
            navigateMaze(arm, path) # have the arm navigate the solution through the maze
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
