from xarm import Controller
from xarm.servo import Servo

class student_controller(Controller):
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

    def home_arm(self):
        self.setPosition(self.art1["Servo Number"], 1500, wait=False)
        self.setPosition(self.art2["Servo Number"], 1500, wait=False)
        self.setPosition(self.art3["Servo Number"], 1500, wait=False)
        self.setPosition(self.art4["Servo Number"], 1500, wait=False)
        self.setPosition(self.art5["Servo Number"], 1500, wait=False)
        self.setPosition(self.claw["Servo Number"], 2500, wait=False)

if __name__ == "__main__":
    port = "USB"  # Replace with the correct port
    controller = student_controller(port)
    battery_voltage = controller.getBatteryVoltage()
    print('Battery voltage (volts):', battery_voltage) # plugged into wall returns 7.411 (volts)

    input("Press Enter to continue...")
    controller.home_arm()
    input("Press Enter to continue...")

