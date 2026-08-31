import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from smart_assistant import SmartAssistant


class SmartAssistantTests(unittest.TestCase):
    def setUp(self):
        self.assistant = SmartAssistant()

    def test_percentage_request(self):
        self.assertIn("Answer: 200", self.assistant.solve("25% of 800"))

    def test_square_root_request(self):
        self.assertIn("Answer: 12", self.assistant.solve("square root of 144"))

    def test_arithmetic_request(self):
        self.assertIn("14", self.assistant.solve("2 + 3 * 4"))

    def test_equation_request(self):
        response = self.assistant.solve("2*x + 3 = 7")
        self.assertIn("x = 2", response)
        self.assertIn("Divide both sides", response)

    def test_equation_explains_each_step(self):
        response = self.assistant.solve("2*x + 5 = 15")
        self.assertIn("Move the constant term: 2x = 10", response)
        self.assertIn("Divide both sides by 2: x = 5", response)

    def test_natural_scientific_questions(self):
        self.assertIn("Answer: 1", self.assistant.solve("what is sin of 90"))
        self.assertIn("Answer: 8", self.assistant.solve("2 raised to the power 3"))

    def test_solve_prefix_is_supported(self):
        self.assertIn("x = 3", self.assistant.solve("solve 3*x - 9 = 0"))

    def test_unsafe_input_is_rejected(self):
        response = self.assistant.solve('__import__("os").getcwd()')
        self.assertIn("couldn't evaluate", response)

    def test_invalid_arithmetic_is_reported(self):
        response = self.assistant.solve("1 / 0")
        self.assertIn("couldn't evaluate", response)

    def test_average_and_conversion(self):
        average = self.assistant.solve("average of 10, 20, 30")
        conversion = self.assistant.solve("convert 10 km to mi")
        self.assertIn("Answer: 20", average)
        self.assertIn("Explanation:", average)
        self.assertIn("6.2137119224 mi", conversion)
        self.assertIn("Explanation:", conversion)


if __name__ == "__main__":
    unittest.main()