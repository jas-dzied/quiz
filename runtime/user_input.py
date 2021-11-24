"""
user_input- contains methods and classes for user input
This includes menu selections and different questions
"""

import string
from abc import ABC, abstractmethod

def invalid_choice(number):
    """Displays an invalid choice message"""
    print(f"That is not a valid choice. Please provide a number in the range: 1-{number}.")

INVALID_MESSAGE = 'That is not a valid choice.\
 Please select an option from the list above or its corresponding letter.'

def choose_menu(prompt: str, options: list[str], default: int) -> str:
    """Displays a menu of options for the user to pick from"""
    print(f'{prompt} (default = {options[default-1]} [{default}]):')
    for i, option in enumerate(options):
        print(f' [{i+1}] {option}')

    while True:
        choice = input(' :: ')
        if choice.isnumeric():
            if int(choice) in list(range(1, len(options)+1)):
                result = options[int(choice)-1]
                print(f" Selected: {repr(result)}")
                return result
            invalid_choice(len(options))
        elif choice == "":
            result = options[default-1]
            print(f" Selected: {repr(result)}")
            return result
        if choice in options:
            print(f" Selected: {repr(choice)}")
            return choice
        print("That is not a valid choice. Please select an option from the list above.")

    return result

def correct_answer() -> None:
    """A simple message that displays when the user gets an answer correct"""
    print(" Correct!")

class Question(ABC):
    """An Abstract Base Class that represents any kind of quiz question"""

    @abstractmethod
    def ask(self, number: int) -> int:
        """Asks a user the question"""
        return 0

    def __init__(self, answer: str) -> None:
        self.answer = answer
    def wrong_answer(self) -> None:
        """Displays a message with the correct answer"""
        print(f" Wrong! The correct answer was: {self.answer}")

class MultipleChoice(Question):
    """A type of question where the user picks from a list"""
    def __init__(self, prompt: str, options: list[str], answer: str) -> None:
        self.prompt = prompt
        self.options = options
        self.answer = answer
        super().__init__(answer)
    def ask(self, number) -> int:
        print(f"==QUESTION {number}== (type = multiple choice)")
        print(f" {self.prompt}")
        for letter, option in zip(string.ascii_letters, self.options):
            print(f' [{letter}] {option}')

        while True:
            choice = input(' :: ')
            if choice in self.options:
                if choice.lower().strip() == self.answer.lower().strip():
                    correct_answer()
                    return 1
                self.wrong_answer()
                return 0
            if choice in string.ascii_letters[:len(self.options)]:
                if self.options[string.ascii_letters.index(choice)] == self.answer:
                    correct_answer()
                    return 1
                self.wrong_answer()
                return 0
            print(INVALID_MESSAGE)
class SingleAnswer(Question):
    """
    A type of question where there is only one correct answer
    The user enters a single value, and the program checks if it is correct
    """
    def __init__(self, prompt: str, answer: str) -> None:
        self.prompt = prompt
        self.answer = answer
        super().__init__(answer)
    def ask(self, number: int) -> int:
        print(f"==QUESTION {number}== (type = single answer)")
        print(f" {self.prompt}")
        choice = input(' :: ')
        if choice.lower() == self.answer.lower():
            correct_answer()
            return 1
        self.wrong_answer()
        return 0
class Options(Question):
    """A type of question where there are several possible answers"""
    def __init__(self, prompt: str, answers: list[str]) -> None:
        self.prompt = prompt
        self.answers = answers
        super().__init__("")
    def wrong_answer(self):
        print(" Wrong! The available answers were: ")
        for answer in self.answers:
            print(f"  {answer}")
    def ask(self, number: int) -> int:
        print(f"==QUESTION {number}== (type = options)")
        print(f" {self.prompt}")
        choice = input(' :: ')
        if choice.lower() in map(lambda x: x.lower(), self.answers):
            correct_answer()
            return 1
        self.wrong_answer()
        return 0
