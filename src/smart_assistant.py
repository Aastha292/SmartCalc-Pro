"""
smart_assistant.py
Smart mathematical assistant for SmartCalc Pro
"""

import math
import sympy as sp
import re


class SmartAssistant:

    def __init__(self):
        self.last_query = ""
        self.last_result = None

    def solve(self, query):
        """
        Understand a simple natural-language math request
        and return a useful answer.
        """

        self.last_query = query.strip()

        if not self.last_query:
            return "Please enter a mathematical question."

        text = self.last_query.lower().strip()

        try:
            text = re.sub(r"^(what is|calculate|evaluate|please calculate|solve)\s+", "", text)

            stats_match = re.fullmatch(r"(?:mean|average|avg)\s+of\s+([0-9.,\s-]+)", text)
            if stats_match:
                values = [float(value) for value in re.findall(r"-?\d+(?:\.\d+)?", stats_match.group(1))]
                if not values:
                    raise ValueError("No values supplied")
                result = sum(values) / len(values)
                self.last_result = result
                total = self.format_result(sum(values))
                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    "Explanation:\n"
                    f"Add the values: {total}.\n"
                    f"Divide by {len(values)} values: {total} / {len(values)} = "
                    f"{self.format_result(result)}."
                )

            conversion_match = re.fullmatch(
                r"convert\s+(-?\d+(?:\.\d+)?)\s*(km|mi|m|ft|kg|lb|c|f)\s+(?:to|in)\s+(km|mi|m|ft|kg|lb|c|f)",
                text,
            )
            if conversion_match:
                amount = float(conversion_match.group(1))
                source, target = conversion_match.group(2), conversion_match.group(3)
                result = self.convert(amount, source, target)
                self.last_result = result
                return (
                    f"Answer: {self.format_result(result)} {target}\n\n"
                    "Explanation:\n"
                    f"Convert {self.format_result(amount)} {source} into {target} "
                    f"using the standard conversion factor."
                )

            # ---------------------------------
            # Percentage requests
            # ---------------------------------
            percentage_match = re.search(
                r"(\d+(?:\.\d+)?)\s*%\s*(?:of)\s*(\d+(?:\.\d+)?)",
                text
            )

            if percentage_match:
                percent = float(percentage_match.group(1))
                number = float(percentage_match.group(2))

                result = (percent / 100) * number
                self.last_result = result

                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    f"Explanation:\n"
                    f"{percent}% means {percent}/100.\n"
                    f"{number} × {percent}/100 = "
                    f"{self.format_result(result)}"
                )

            # ---------------------------------
            # Square root
            # ---------------------------------
            sqrt_match = re.search(
                r"(?:sqrt|square root of)\s*(\d+(?:\.\d+)?)",
                text
            )

            if sqrt_match:
                number = float(sqrt_match.group(1))

                result = math.sqrt(number)
                self.last_result = result

                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    f"Explanation:\n"
                    f"The square root of {number} is "
                    f"{self.format_result(result)}."
                )

            scientific_match = re.fullmatch(
                r"(?:value of |find )?(sin|cos|tan|log|ln|factorial)\s*(?:of\s*)?\(?(-?\d+(?:\.\d+)?)\)?",
                text,
            )
            if scientific_match:
                function, number_text = scientific_match.groups()
                number = float(number_text)
                if function == "factorial":
                    if number < 0 or not number.is_integer():
                        raise ValueError("Factorial requires a non-negative integer")
                    result = math.factorial(int(number))
                    explanation = f"Multiply the integers from 1 through {int(number)}."
                elif function == "sin":
                    result = math.sin(math.radians(number))
                    explanation = "For this assistant request, the angle is interpreted in degrees."
                elif function == "cos":
                    result = math.cos(math.radians(number))
                    explanation = "For this assistant request, the angle is interpreted in degrees."
                elif function == "tan":
                    result = math.tan(math.radians(number))
                    explanation = "For this assistant request, the angle is interpreted in degrees."
                elif function == "log":
                    result = math.log10(number)
                    explanation = "Log means the base-10 logarithm."
                else:
                    result = math.log(number)
                    explanation = "ln means the natural logarithm."
                self.last_result = result
                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    f"Explanation:\n{explanation}\n"
                    f"{function}({self.format_result(number)}) = {self.format_result(result)}"
                )

            power_match = re.fullmatch(
                r"(-?\d+(?:\.\d+)?)\s+raised\s+to\s+(?:the\s+)?(?:power\s+)?(-?\d+(?:\.\d+)?)",
                text,
            )
            if power_match:
                base, exponent = (float(value) for value in power_match.groups())
                result = base ** exponent
                self.last_result = result
                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    f"Explanation:\nRaise the base to the exponent: "
                    f"{self.format_result(base)}^{self.format_result(exponent)} = "
                    f"{self.format_result(result)}"
                )

            # ---------------------------------
            # Equation solver
            # ---------------------------------
            if "=" in text:
                equation = text.replace("^", "**")
                if not re.fullmatch(r"[0-9x+*/().\s*-]+=[0-9x+*/().\s*-]+", equation):
                    raise ValueError("Unsupported equation characters")
                left_side, right_side = equation.split("=", 1)
                x = sp.Symbol("x")
                left_expr = sp.sympify(left_side)
                right_expr = sp.sympify(right_side)
                solutions = sp.solve(sp.Eq(left_expr, right_expr), x)

                if solutions:
                    self.last_result = solutions[0]
                    formatted = ", ".join(str(solution) for solution in solutions)
                    return self.explain_equation(left_expr, right_expr, solutions, formatted)

                return "No solution found for that equation."

            # ---------------------------------
            # Simple arithmetic
            # ---------------------------------
            expression = text

            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("−", "-")

            expression = re.sub(r"[^0-9+\-*/().%\s]", "", expression)

            if expression.strip():
                result = sp.sympify(expression)
                if not result.is_number or result.is_finite is False:
                    raise ValueError("Expression is not numeric")
                result = result.evalf()

                self.last_result = result

                return (
                    f"Answer: {self.format_result(result)}\n\n"
                    "Explanation:\n"
                    "Evaluate multiplication, division, and powers before addition and subtraction.\n"
                    f"{expression} = "
                    f"{self.format_result(result)}"
                )

        except (ValueError, TypeError, SyntaxError, ZeroDivisionError, OverflowError, sp.SympifyError):
            return "I couldn't evaluate that safely. Please enter a valid math expression."

        return (
            "I couldn't understand that request yet.\n\n"
            "Try examples such as:\n"
            "• 25% of 800\n"
            "• square root of 144\n"
            "• 25 × 4"
        )

    # ---------------------------------
    # Result formatting
    # ---------------------------------

    def explain_equation(self, left_expr, right_expr, solutions, formatted):
        equation = sp.expand(left_expr - right_expr)
        variable = sp.Symbol("x")
        polynomial = sp.Poly(equation, variable)

        if polynomial.degree() == 1:
            coefficient = polynomial.coeff_monomial(variable)
            constant = polynomial.coeff_monomial(1)
            remaining = -constant
            return (
                f"Answer: x = {formatted}\n\n"
                "Explanation:\n"
                f"Start with: {left_expr} = {right_expr}\n"
                f"Move the constant term: {coefficient}x = {remaining}\n"
                f"Divide both sides by {coefficient}: x = {formatted}\n"
                "Equation solved successfully."
            )

        if polynomial.degree() > 1:
            factored = sp.factor(equation)
            return (
                f"Answer: x = {formatted}\n\n"
                "Explanation:\n"
                f"Rewrite the equation as: {equation} = 0\n"
                f"Factor or simplify: {factored} = 0\n"
                f"The resulting roots are x = {formatted}."
            )

        return (
            f"Answer: x = {formatted}\n\n"
            "Explanation:\n"
            f"Solve {left_expr} = {right_expr} and verify the solution in the original equation."
        )

    def convert(self, amount, source, target):
        if source == target:
            return amount
        if {source, target} == {"c", "f"}:
            return (amount * 9 / 5 + 32) if source == "c" else (amount - 32) * 5 / 9
        units = {
            "m": 1, "km": 1000, "mi": 1609.344, "ft": 0.3048,
            "kg": 1, "lb": 0.45359237,
        }
        if source not in units or target not in units or (source in {"m", "km", "mi", "ft"}) != (target in {"m", "km", "mi", "ft"}):
            raise ValueError("Incompatible units")
        return amount * units[source] / units[target]

    def format_result(self, result):

        if isinstance(result, (float, sp.Float)):
            result = float(result)

            if result.is_integer():
                return str(int(result))

            return str(round(result, 10))

        return str(result)