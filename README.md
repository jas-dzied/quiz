# Quiz

Quiz is a collection of programs for text-based quizzes. It currently is made up of 2 main projects, `runtime` and `quiz-compiler`.

## Runtime

The runtim uses a `.json` file to generate a list of quizzes, with each quiz containing its own list of questions.

##### Usage

2 files are provided, `main.py` and `user_input.py`. They should be put in the same directory to work, along with the `questions.json` file.

You can run the `main.py` file with `python runtime/main.py` to start the quiz. You should specify a path to the `questions.json` file. If you don't, the default one will be used, which probably won't work for you.

##### Formatting

The code is completely type hinted and follows PEP guidelines:

`mypy main.py` output: `Success: no issues found in 1 source file`

`mypy user_input.py` output: `Success: no issues found in 1 source file`


`python -m pylint main.py` output: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

`python -m pylint user_input.py` output: `Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)`

##### Creating quiz questions

The `questions.json` file follows a simple format:

At the top level, it is a set of objects, using strings as keys and lists as values.

The lists are a list of questions, which are also objects. They all have a `type` key and a `prompt` key, as well as any question-specific keys. The `prompt` key contains the message displayed to the user. The available types are:

| Type            | Description                                                                                           | Keys                                  |
| --------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------- |
| multiple choice | Takes in a list of options and presents them to the user to pick from.                                | `type`, `prompt`, `options`, `answer` |
| single answer   | Takes a single input from the user and compares it to the correct answer.                             | `type`, `prompt`, `answer`            |
| options         | Takes in a single input and checks if it is in the provided list of strings that are correct answers. | `type`, `prompt`, `answers`           |

#### Testing

A `test.py` file is provided which contains unit tests for the questions. This can be run with `python runtime/test.py`.

## Quiz-compiler

This program converts a `.qz` file to a `.json` file that can be run by the runtime.

##### Usage

The compiler is written in Rust, so it can be run with `cargo run` while in the `quiz-compiler directory`. You should provide a path to the source file, and optionally one to the destination file.

The `.qz` should follow the format:

A list of quizzes, seperated by `###`

Each quiz is made up of a list of questions, seperated by `~~~`

(The first question in each quiz should just be a single line containing the name of the quiz)

Each question follows the format:

- Line 1: Type of question (multiple choice, single answer, options)
- Line 2: Prompt (the message that is displayed when the question is asked)
- Lines 3..: Any question-type specific parameters.
 - For `multiple choice`, provide a correct answer and then a list of possible answers.
 - For `single answer`, provide the correct answer.
 - For `options`, provide a list of possible answers.
 
A example question would be:

```
multiple choice
What is the largest country in the world?
Russia
China
Russia
Canada
Australia
```
