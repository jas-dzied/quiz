"""Quiz- A python program that uses a JSON file containing quiz questions to test the user"""

import json
import sys
from user_input import Question, choose_menu, MultipleChoice, SingleAnswer, Options

def ask_questions(questions: list[Question]) -> None:
    """
    Takes in a list of questions, and asks each of them to the user.
    It also keeps track of the score throughout.
    """
    score = 0
    for i, question in enumerate(questions):
        score += question.ask(i+1)
        print(f"Your current score is: {score}/{i+1}")
        print()
    print()
    print("Your overall score was:")
    print(f"{score}/{len(questions)}")
    percentage = round(score/len(questions) * 100)
    print(f"{percentage}%")
    if percentage == 100:
        print("Perfect!")
    else:
        print("Better luck next time!")

def start_quiz(quiz_list: dict[str, list[Question]]) -> None:
    """
    Allows the user to choose from a list of possible quizzes.
    It also starts the specific quiz that was chose
    """
    chosen_quiz = choose_menu("Which quiz would you like to do?", list(quiz_list.keys()), 1)
    print()
    ask_questions(quiz_list[chosen_quiz])

def generate_questions(file_path: str) -> dict[str, list[Question]]:
    """Generates a set of quizzes based off a JSON file"""
    with open(file_path, 'r', encoding="utf-8") as file:
        data = json.load(file)
    result = {}
    for name, questions in data.items():
        question_list: list[Question] = []
        for question in questions:
            if question["type"] == "multiple choice":
                qst = MultipleChoice(question["prompt"], question["options"], question["answer"])
                question_list.append(qst)
            elif question["type"] == "options":
                question_list.append(Options(question["prompt"], question["answers"]))
            elif question["type"] == "single answer":
                question_list.append(SingleAnswer(question["prompt"], question["answer"]))
            else:
                print(f"Unknown question type: {question['type']}")
                sys.exit(1)
        result[name] = question_list
    return result

DEFAULT_PATH = "/home/jas/Documents/Programming/Projects/quiz/questions.json"

if __name__ == '__main__':
    questions_path = sys.argv[1] if len(sys.argv) != 1 else DEFAULT_PATH
    quizzes = generate_questions(questions_path)
    start_quiz(quizzes)
