import unittest
from unittest.mock import patch

from user_input import MultipleChoice, SingleAnswer, Options

class TestInputMethods(unittest.TestCase):

    @patch('user_input.print', lambda x: x)
    def test_multiple_choice(self):
        question = MultipleChoice("prompt", ["option 1", "option 2"], "option 1")
        with patch("user_input.input", lambda prompt="": "a"):
            result = question.ask(0)
            self.assertEqual(result, 1)
        with patch("user_input.input", lambda prompt="": "b"):
            result = question.ask(0)
            self.assertEqual(result, 0)

    @patch('user_input.print', lambda x: x)
    def test_single_answer(self):
        question = SingleAnswer("prompt", "answer")
        with patch("user_input.input", lambda prompt="": "answer"):
            result = question.ask(0)
            self.assertEqual(result, 1)
        with patch("user_input.input", lambda prompt="": "wrong answer"):
            result = question.ask(0)
            self.assertEqual(result, 0)

    @patch('user_input.print', lambda x: x)
    def test_options(self):
        question = Options("prompt", ["answer1", "answer2", "answer3"])
        with patch("user_input.input", lambda prompt="": "answer1"):
            result = question.ask(0)
            self.assertEqual(result, 1)
        with patch("user_input.input", lambda prompt="": "answer2"):
            result = question.ask(0)
            self.assertEqual(result, 1)
        with patch("user_input.input", lambda prompt="": "wrong answer"):
            result = question.ask(0)
            self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()
