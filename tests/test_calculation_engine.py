import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from calculation_engine import CalculationEngine, CalculationError


class CalculationEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = CalculationEngine()

    def test_scientific_operations(self):
        self.assertEqual(self.engine.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.engine.evaluate("5!"), 120)
        self.assertEqual(self.engine.evaluate("sin(90)"), 1)
        self.assertAlmostEqual(self.engine.evaluate("sin(pi / 2)", "RAD"), 1)

    def test_unsafe_expression_is_rejected(self):
        with self.assertRaises(CalculationError):
            self.engine.evaluate("__import__('os').system('echo bad')")

    def test_invalid_factorial_is_rejected(self):
        with self.assertRaises(CalculationError):
            self.engine.evaluate("3.5!")