# This file will allow the user to play a game of simon says with the robot arm

import time
import random
from robotArm import RobotArm

MISTAKE_THRESHOLD = 0.2


class SimonSays:
    def __init__(self, port):
        try:
            self.arm = RobotArm(port)
        except:
            print("Could not connect to the robot arm. Please check the connection and try again.")
            return
        self.arm.home_arm()

    def parse_input(input_string):
        # split the input into words
        words = input_string.split()

        # Remove punctuation
        words = [word.strip(",.?!") for word in words]

        # Filter out any insignificant words
        significant_words = [word for word in words if word.lower() not in ["the", "and", "or", "a", "an"]]

        return significant_words
    
    def execute_input(self, user_input):
        # Parse the input
        significant_words = self.parse_input(user_input)

        # if the first two words are "simon says", follow them -> random amount of mess ups
        if significant_words[:2] == ["simon", "says"]:
            if random.random() < MISTAKE_THRESHOLD: # chance of not executing when it should INTENTIONAL
                print("I never heard you say simon says! I'm not going to do that.")
                return
            else:
                significant_words = significant_words[2:]
        else:
            if random.random() < (1 - MISTAKE_THRESHOLD): # chance of executing when it shouldn't INTENTIONAL
                print("I only do what Simon says. I'm not going to do that.")
                return

        # Execute the command
        if "move" in significant_words:
            self.move_arm(significant_words)
        elif "say" in significant_words:
            self.say_something(significant_words)
        elif "wave" == significant_words[0]: # "Simon says wave" | "wave"
            self.arm.wave()
        elif ("home" in significant_words) and ("arm" in significant_words): # "Simon says home arm" | "home arm"
            self.arm.home_arm()
        elif ("set" in significant_words) and ("saved" in significant_words) and ("position" in significant_words):
            self.go_to_saved_position(significant_words)
        else:
            print("I'm sorry, I don't understand that command.")

    def _word_to_number(self, word):
        word_to_number_dict = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                            "six": 6, "seven": 7, "eight": 8, "nine": 9, "zero": 0}
        return word_to_number_dict.get(word.lower())

    def move_arm(self, significant_words):
        # find the proper articulation number
        articulation_number = significant_words[significant_words.index("articulation") + 1]
        articulation_number = self._word_to_number(articulation_number)
        
        # find the proper position number
        position_number = significant_words[significant_words.index("position") + 1]
        position_number = self._word_to_number(position_number)

        # move the arm
        self.arm.setArticulation(articulation_number, position_number)

    def say_something(self, significant_words):
        # find the proper phrase
        phrase = " ".join(significant_words[significant_words.index("say") + 1:])
        print("Speaking: " + phrase)

        # say the phrase
        self.arm.speak(phrase)

    def wave_command(self, significant_words):
        # call the wave function
        self.arm.wave()

    def go_to_saved_position(self, significant_words):
        # find the name of the saved position
        position_name = significant_words[significant_words.index("position") + 1]
        
        # go to the saved position
        self.arm.loadPositionSettings(position_name)

    def play_game(self):
        # start game
        print("Thank you for playing Simon Says with me. \nYou will tell me what to do and I will try and follow it until I lose! \nLet's get started!")
        time.sleep(1)

        # keep playing until the user quits
        while True:
            user_input = input("What should I do? ")
            if user_input.lower() == "quit":
                break
            self.execute_input(user_input)

        # end game
        print("Thanks for playing Simon Says with me! I hope you had fun as well!")


if __name__ == "__main__":
    simon_says = SimonSays("USB")
    simon_says.play_game()

