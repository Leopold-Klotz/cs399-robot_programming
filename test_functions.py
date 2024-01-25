import xarm

arm = xarm.Controller('USB')

battery_voltage = arm.getBatteryVoltage()
print('Battery voltage (volts):', battery_voltage) # plugged into wall returns 7.411 (volts)


'''
Basic information:
Art 1 = Servo 6 Base. Range 500-2500. 500 full CW (top down view), 2500 full CCW (top down view)
Art 2 = Servo 5. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
Art 3 = Servo 4. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
Art 4 = Servo 3. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
Art 5 = Servo 2. Range 500-2500. 500 full CCW (from servo pov), 2500 full CW (from servo pov).
Claw = Servo 1. Range 1000-2500. 1000 is closed, 2500 is open.

'''


while True:
    servo_number = input("Enter servo number (1-6): ")
    position_number = input("Enter position number: ")
    
    try:
        servo_number = int(servo_number)
        position_number = int(position_number)
        
        arm.setPosition(servo_number, position_number, wait=False)
        print("Servo", servo_number, "position set to", position_number)
        print("get position: ", arm.getPosition(servo_number))
    except ValueError:
        print("Invalid input. Please enter a valid servo number and position number.")
