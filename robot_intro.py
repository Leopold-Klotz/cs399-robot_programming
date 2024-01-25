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

    def savePositionSettings(self):
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
                claw_position = positions.get("Claw")
                if claw_position is not None:
                    self.setClaw(claw_position, wait=False)
            else:
                print(f"No positions found for {name}")
        time.sleep(0.5)

        
    # Set all of the articulation positions to upright and their middle values.
    def home_arm(self):
        self.setArt1(1500, wait=False)
        self.setArt2(1500, wait=False)
        self.setArt3(1500, wait=False)
        self.setArt4(1500, wait=False)
        self.setArt5(1500, wait=False)

    def say_hello(self):
        engine = pyttsx3.init()
        engine.say("Hello, my name is Xarm. I am a robot arm.")
        engine.runAndWait()

    def speak(self, text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    # Wave to the user 3 times
    def wave(self):
        # speech thread
        speech_thread = threading.Thread(target=self.say_hello)

        # wave sequence
        self.home_arm()
        time.sleep(1)
        speech_thread.start() # start speaking
        for _ in range(2):  # Loop through the sequence to wave
            self.setArt5(1000, wait=False)
            self.setArt3(1000, wait=False)
            self.setArt4(2000, wait=False)
            self.setArt5(2000, wait=False)
            time.sleep(1)
            self.setArt5(1000, wait=False)
            self.setArt3(2000, wait=False)
            self.setArt4(1000, wait=False)
            self.setArt5(2000, wait=False)
            time.sleep(1)
        self.home_arm()

        speech_thread.join() # wait for the speaking to finish


if __name__ == "__main__":
    port = "USB"  # Replace with the correct port
    arm = RobotArm(port)
    battery_voltage = arm.getBatteryVoltage()
    print('Battery voltage (volts):', battery_voltage) # plugged into wall returns 7.411 (volts)

    input1 = input("Press 'h' to home arm...\n'w' to wave...\n")
    if input1 == "h":
        arm.home_arm()
    elif input1 == "w":
        arm.wave()
    input("Press Enter to continue...")

    while True:
        articulation_number = input("Enter articulation number (0-5): ")
        position_number = input("Enter position number: ")
        
        try:
            articulation_number = int(articulation_number)
            position_number = int(position_number)
            
            if articulation_number == 0:
                arm.savePositionSettings()
            elif articulation_number == 1:
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
                print("Invalid articulation number. Please enter a number between 0 and 5.")

        except ValueError:
            print("Invalid input. Please enter a valid articulation number and position number.")

