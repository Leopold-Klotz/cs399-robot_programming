from maze_recognition.map import Map
from robotArm import RobotArm
from maze_recognition.camera import Camera_Sensor
from maze_recognition.remove_border import remove_maze_border
import time

def scan_new_maze():
    # Code to scan a new maze
    print("Scanning new maze")
    
    # initializing camera sensor
    print("Initializing camera sensor...")
    camera = Camera_Sensor()
    if camera.detect_paper_loop("new_maze.png") == 0:
        print("Maze successfully scanned")
        print("Removing maze border...")
        if remove_maze_border("new_maze.png", "edged_maze.png") == 0:
            print("Border removed successfully")
            return 0

        else:
            print("Error: Maze border could not be removed")

    else:
        print("Error: Maze could not be scanned")
    return 1

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
    arm = None
    try:
        arm = RobotArm(port)
    except:
        print("Error: Could not connect to the robot arm")
        
    map = Map(4, 4)  

    while True:
        choice = input("Enter '1' to scan a new maze or '2' to travel a known maze ('3' to exit): ")

        if choice == '1':
            arm.home_arm()
            if scan_new_maze() != 0:
                print("Error scanning maze, maybe visit a known maze.")
            else:
                print("Populating map with maze information...")
                map.populate_map('edged_maze.png')
                map.print_map()
                map.solve_map()
                map.print_solution()
                path = map.get_Solution()
                navigateMaze(arm, path) # have arm go through the maze

        elif choice == '2':
            maze_choice = input("Enter the maze number (1, 2, 3, etc.): ")
            maze_choice = "maze_recognition/random_maze" + str(maze_choice) + ".png"
            map.populate_map(maze_choice)
            map.print_map()
            map.solve_map()
            path = map.get_Solution()
            navigateMaze(arm, path) # have the arm navigate the solution through the maze
        
        elif choice == '3':
            exit()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
