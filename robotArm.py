# Author: Leopold Klotz
# Email: klotzl@oregonstate.edu

from xarm import Controller
import time
import pyttsx3
import threading
import json

class RobotArm(Controller):
    '''
    Basic information:
    Art 1 = Servo 6 Base. Range 500-2500. 500 full CW (top down view), 2500 full CCW (top down view)
    Art 2 = Servo 5. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
    Art 3 = Servo 4. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
    Art 4 = Servo 3. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
    Art 5 = Servo 2. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
    Claw = Servo 1. Range 1000-2500. 1000 is closed, 2500 is open.

    '''
    def __init__(self, port):
        super().__init__(port)
        self.art1 = {"Servo Number": 6, "Position": None}
        self.art2 = {"Servo Number": 5, "Position": None}
        self.art3 = {"Servo Number": 4, "Position": None}
        self.art4 = {"Servo Number": 3, "Position": None}
        self.art5 = {"Servo Number": 2, "Position": None}
        self.claw = {"Servo Number": 1, "Position": None}

    """
    Articulation Functions: control the arm's articulations as opposed to the specific servo number.
        The purpose of creation was to get around the lack of position saving functionality for the
        LeArm in the xArm package.
        input: position (int) - the position to move the articulation to
        input: wait (bool) - whether or not to wait for the arm to reach the position
        result: moves the articulation to the specified position (saves the position in the articulation's 
            dictionary)
    """

    def setArt1(self, position, wait=False):
        self.setPosition(self.art1["Servo Number"], position, wait=wait)
        self.art1["Position"] = position
        time.sleep(0.5)

    def setArt2(self, position, wait=False):
        self.setPosition(self.art2["Servo Number"], position, wait=wait)
        self.art2["Position"] = position
        time.sleep(0.5)

    def setArt3(self, position, wait=False):
        self.setPosition(self.art3["Servo Number"], position, wait=wait)
        self.art3["Position"] = position
        time.sleep(0.5)

    def setArt4(self, position, wait=False):
        self.setPosition(self.art4["Servo Number"], position, wait=wait)
        self.art4["Position"] = position
        time.sleep(0.5)

    def setArt5(self, position, wait=False):
        self.setPosition(self.art5["Servo Number"], position, wait=wait)
        self.art5["Position"] = position
        time.sleep(0.5)

    def setClaw(self, position, wait=False):
        self.setPosition(self.claw["Servo Number"], position, wait=wait)
        self.claw["Position"] = position
        time.sleep(0.5)

    def getArticulation(self, articulation):
        """
        Returns the current position of the specified articulation.
            inputs: articulation (int) - the articulation number to get the position of
            result: returns the position of the specified articulation
        """
        if articulation == 1:
            return self.art1["Position"]
        elif articulation == 2:
            return self.art2["Position"]
        elif articulation == 3:
            return self.art3["Position"]
        elif articulation == 4:
            return self.art4["Position"]
        elif articulation == 5:
            return self.art5["Position"]
        elif articulation == 6:
            return self.claw["Position"]
        else:
            print("Invalid articulation number. Please enter a number between 1 and 6.")

    def setArticulation(self, articulation, position, wait=False):
        """
        Moves the specified articulation to the specified position.
            inputs: articulation (int) - the articulation number to move
            inputs: position (int) - the position to move the articulation to
            inputs: wait (bool) - whether or not to wait for the arm to reach the position
            result: moves the articulation to the specified position (saves the position in the articulation's 
                dictionary)
        """
        if articulation == 1:
            self.setArt1(position, wait=wait)
        elif articulation == 2:
            self.setArt2(position, wait=wait)
        elif articulation == 3:
            self.setArt3(position, wait=wait)
        elif articulation == 4:
            self.setArt4(position, wait=wait)
        elif articulation == 5:
            self.setArt5(position, wait=wait)
        elif articulation == 6:
            # flip position for claw 500= open, 2500 = closed
            position = 3000 - position
            self.setClaw(int(position), wait=wait)
        else:
            print("Invalid articulation number. Please enter a number between 1 and 6.")

    def savePositionSettings(self):
        """
        Saves the current positions of the arm's articulations to a file called saved_positions.json
            inputs: user input for the name of the position to save. 
            result: saves the position to saved_positions.json
        """
        name = input("Enter a name for the position settings: ")
        positions = {
            "Art1": self.art1["Position"],
            "Art2": self.art2["Position"],
            "Art3": self.art3["Position"],
            "Art4": self.art4["Position"],
            "Art5": self.art5["Position"],
            "Claw": self.claw["Position"]
        }

        with open("saved_positions.json", "r+") as file:
            try:
                saved_positions = json.load(file)
            except json.JSONDecodeError:
                saved_positions = {"positions": {}}

            saved_positions["positions"][name] = positions
            file.seek(0)
            json.dump(saved_positions, file, indent=2)
            file.truncate()

    def loadPositionSettings(self, name):
        """
        Loads the positions of the arm's articulations from a file called saved_positions.json
            inputs: (str) the name of the position to load.
            result: moves the arm the position from saved_positions.json
        """
        with open("saved_positions.json", "r") as file:
            try:
                saved_positions = json.load(file)
            except json.JSONDecodeError:
                saved_positions = {"positions": {}}

            positions = saved_positions["positions"].get(name)
            if positions is not None:
                print(f"Trying to parse: {positions}")
                self.setArt1(positions.get("Art1", 0), wait=False)
                self.setArt2(positions.get("Art2", 0), wait=False)
                self.setArt3(positions.get("Art3", 0), wait=False)
                self.setArt4(positions.get("Art4", 0), wait=False)
                self.setArt5(positions.get("Art5", 0), wait=False)
                self.setClaw(positions.get("Claw", 0), wait=False)
                claw_position = positions.get("Claw")
                if claw_position is not None:
                    self.setClaw(claw_position, wait=False)
            else:
                print(f"No positions found for {name}")
        time.sleep(0.5)

    def adjust_saved_position(self, name, articulation, position):
        """
        Adjusts the position of the specified articulation in the specified saved position.
            inputs: name (str) - the name of the position to adjust
            inputs: articulation (int) - the articulation number to adjust
            inputs: position (int) - the new position to set the articulation to
            result: updates the position of the specified articulation in the specified saved position
        """
        with open("saved_positions.json", "r") as file:
            saved_positions = json.load(file)
            positions = saved_positions["positions"].get(name)
            if positions is not None:
                positions[articulation] = position
                saved_positions["positions"][name] = positions
                with open("saved_positions.json", "w") as file:
                    json.dump(saved_positions, file, indent=2)
            else:
                print(f"No positions found for {name}")

    def home_arm(self):
        """
        Moves the arm to the home position (all articulations at 1500, claw at 1500) (straight up).
        """
        self.setArt1(1500, wait=False)
        self.setArt2(1500, wait=False)
        self.setArt3(1500, wait=False)
        self.setArt4(1500, wait=False)
        self.setArt5(1500, wait=False)

    def say_hello(self):
        """Speak a greeting."""
        engine = pyttsx3.init()
        engine.say("Hello, my name is X-arm. I am a robot arm.")
        engine.runAndWait()

    def speak(self, text):
        """
        Speak the input text.
            input: text (str) - the text to speak
            result: speaks the input text through computer speakers
        """
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def wave(self):
        """
        Wave the arm (twice).
        """
        # speech thread
        speech_thread = threading.Thread(target=self.say_hello)

        # wave sequence
        self.home_arm()
        time.sleep(1)
        speech_thread.start() # start speaking
        for _ in range(2):  # Loop through the sequence to wave
            self.setPosition([[2, 1000], [3, 2000], [4, 1000]], wait=False)
            time.sleep(1)
            self.setPosition([[2, 2000], [3, 1000], [4, 2000]], wait=False)
            time.sleep(1)
        self.home_arm()

        speech_thread.join() # wait for the speaking to finish

def main():
    port = "USB"  # Replace with the correct port
    arm = RobotArm(port)
    battery_voltage = arm.getBatteryVoltage()
    print('Battery voltage (volts):', battery_voltage) # plugged into wall returns 7.411 (volts)

    while True:
        print("Options:")
        print("1. Home Arm")
        print("2. Wave")
        print("3. Position Control")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            arm.home_arm()
        elif choice == "2":
            arm.wave()
        elif choice == "3":
            while True:
                print("Position Control:")
                print("0. Save Position")
                print("-1. Load Position")
                print("Articulation Number (1-5): Move articulation")
                print("6. Move Claw")
                print("9. Back to main menu")

                control_choice = input("Enter your choice: ")

                if control_choice == "0":
                    arm.savePositionSettings()
                elif control_choice == "-1":
                    position_name = input("Enter the position name to load: ")
                    arm.loadPositionSettings(position_name)
                elif control_choice == "6":
                    claw_position = int(input("Enter the claw position: "))
                    arm.setClaw(claw_position, wait=False)
                elif control_choice == "9":
                    break
                else:
                    # Choose an articulation and move it to a specified position
                    articulation_number = int(control_choice)
                    position_number = int(input("Enter the position number: "))

                    if articulation_number == 1:
                        arm.setArt1(position_number, wait=False)
                    elif articulation_number == 2:
                        arm.setArt2(position_number, wait=False)
                    elif articulation_number == 3:
                        arm.setArt3(position_number, wait=False)
                    elif articulation_number == 4:
                        arm.setArt4(position_number, wait=False)
                    elif articulation_number == 5:
                        arm.setArt5(position_number, wait=False)
                    else:
                        print("Invalid articulation number. Please enter a number between 1 and 5.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a valid option.")

        input("Press Enter to continue...")

if __name__ == "__main__":
    main()

