# Quiz

Quiz is a simple python library for text-based quizzes. It uses a `.json` file to generate a list of quizzes, with each quiz containing its own list of questions.

### Usage

2 files are provided, `main.py` and `user_input.py`. They should be put in the same directory to work, along with the `questions.json` file.

You can run the `main.py` file with `python main.py` to start the quiz.

### Formatting

The code is completely type hinted and follows PEP guidelines:

`mypy main.py` output: `Success: no issues found in 1 source file`

`mypy user_input.py` output: `Success: no issues found in 1 source file`


`python -m pylint main.py` output: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

`python -m pylint user_input.py` output: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

### Creating quiz questions

The `questions.json` file follows a simple format:

At the top level, it is a set of objects, using strings as keys and lists as values.

The lists are a list of questions, which are also objects. They all have a `type` key and a `prompt` key, as well as any question-specific keys. The `prompt` key contains the message displayed to the user. The available types are:

| Type            | Description                                                                                           | Keys                                  |
| --------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------- |
| multiple choice | Takes in a list of options and presents them to the user to pick from.                                | `type`, `prompt`, `options`, `answer` |
| single answer   | Takes a single input from the user and compares it to the correct answer.                             | `type`, `prompt`, `answer`            |
| options         | Takes in a single input and checks if it is in the provided list of strings that are correct answers. | `type`, `prompt`, `answers`           |
