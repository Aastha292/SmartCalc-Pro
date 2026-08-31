import tkinter as tk
import math


class SmartCalcPro:
    def __init__(self, window):
        self.window = window

        # -----------------------------
        # Window configuration
        # -----------------------------
        self.window.title("SmartCalc Pro")
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        self.window.configure(bg="white")

        # -----------------------------
        # Calculator state
        # -----------------------------
        self.expression = ""
        self.history = []

        # -----------------------------
        # Build interface
        # -----------------------------
        self.create_header()
        self.create_display()
        self.create_buttons()

        # Keyboard support
        self.window.bind("<Key>", self.keyboard_input)

    # =============================
    # HEADER
    # =============================

    def create_header(self):
        header = tk.Frame(
            self.window,
            bg="#111827"
        )
        header.pack(fill="x", padx=20, pady=(20, 10))

        title = tk.Label(
            header,
            text="SmartCalc Pro",
            font=("Segoe UI", 24, "bold"),
            bg="#111827",
            fg="white"
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Advanced Scientific Calculator",
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#9CA3AF"
        )
        subtitle.pack(pady=(3, 0))

    # =============================
    # DISPLAY
    # =============================

    def create_display(self):
        display_frame = tk.Frame(
            self.window,
            bg="#1F2937",
            bd=0
        )
        display_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 15)
        )

        self.display = tk.Entry(
            display_frame,
            font=("Segoe UI", 26),
            justify="right",
            bg="white",
            fg="black",
            insertbackground="black",
            relief="flat",
            bd=0
        )

        self.display.pack(
            fill="x",
            padx=15,
            pady=18
        )

    # =============================
    # BUTTON AREA
    # =============================

    def create_buttons(self):
        button_frame = tk.Frame(
            self.window,
            bg="#111827"
        )
        button_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=5
        )

        buttons = [
            ["C", "⌫", "(", ")"],
            ["sin", "cos", "tan", "√"],
            ["log", "ln", "x²", "xʸ"],
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["0", ".", "%", "+"],
            ["π", "e", "!", "="]
        ]

        for row, button_row in enumerate(buttons):
            button_frame.rowconfigure(row, weight=1)

            for column, text in enumerate(button_row):
                button_frame.columnconfigure(column, weight=1)

                button = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 13, "bold"),
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda value=text: self.button_click(value)
                )

                button.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

                self.style_button(button, text)

    # =============================
    # BUTTON STYLING
    # =============================

    def style_button(self, button, text):

        if text in ["+", "−", "×", "÷", "="]:
            button.configure(
                bg="#2563EB",
                fg="white",
                activebackground="#1D4ED8",
                activeforeground="white"
            )

        elif text in ["C", "⌫"]:
            button.configure(
                bg="#DC2626",
                fg="white",
                activebackground="#B91C1C",
                activeforeground="white"
            )

        elif text in [
            "sin", "cos", "tan", "√",
            "log", "ln", "x²", "xʸ",
            "π", "e", "!"
        ]:
            button.configure(
                bg="#374151",
                fg="#93C5FD",
                activebackground="#4B5563",
                activeforeground="white"
            )

        else:
            button.configure(
                bg="#1F2937",
                fg="white",
                activebackground="#374151",
                activeforeground="white"
            )

    # =============================
    # BUTTON LOGIC
    # =============================

    def button_click(self, value):

        if value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "=":
            self.calculate()

        elif value == "√":
            self.add_to_expression("sqrt(")

        elif value == "x²":
            self.add_to_expression("**2")

        elif value == "xʸ":
            self.add_to_expression("**")

        elif value == "sin":
            self.add_to_expression("sin(")

        elif value == "cos":
            self.add_to_expression("cos(")

        elif value == "tan":
            self.add_to_expression("tan(")

        elif value == "log":
            self.add_to_expression("log(")

        elif value == "ln":
            self.add_to_expression("ln(")

        elif value == "π":
            self.add_to_expression("pi")

        elif value == "e":
            self.add_to_expression("e")

        elif value == "!":
            self.add_to_expression("!")

        elif value == "%":
            self.add_to_expression("/100")

        else:
            self.add_to_expression(value)

    # =============================
    # EXPRESSION MANAGEMENT
    # =============================

    def add_to_expression(self, value):
        self.expression += value
        self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def clear(self):
        self.expression = ""
        self.update_display()

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()

    # =============================
    # CALCULATION ENGINE
    # =============================

    def calculate(self):

        if not self.expression:
            return

        try:
            expression = self.expression

            expression = expression.replace("×", "*")
            expression = expression.replace("÷", "/")
            expression = expression.replace("−", "-")

            expression = expression.replace(
                "sin(",
                "math.sin(math.radians("
            )

            expression = expression.replace(
                "cos(",
                "math.cos(math.radians("
            )

            expression = expression.replace(
                "tan(",
                "math.tan(math.radians("
            )

            expression = expression.replace(
                "sqrt(",
                "math.sqrt("
            )

            expression = expression.replace(
                "log(",
                "math.log10("
            )

            expression = expression.replace(
                "ln(",
                "math.log("
            )

            expression = expression.replace(
                "pi",
                "math.pi"
            )

            expression = expression.replace(
                "e",
                "math.e"
            )

            # Factorial support
            if "!" in expression:
                expression = self.process_factorial(expression)

            result = eval(
                expression,
                {
                    "__builtins__": {},
                    "math": math
                }
            )

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.history.append(
                f"{self.expression} = {result}"
            )

            self.expression = str(result)
            self.update_display()

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero.")

        except ValueError:
            self.show_error("Invalid mathematical value.")

        except Exception:
            self.show_error("Invalid expression.")

    # =============================
    # FACTORIAL
    # =============================

    def process_factorial(self, expression):

        while "!" in expression:

            index = expression.index("!")

            number = ""

            i = index - 1

            while i >= 0 and (
                expression[i].isdigit()
                or expression[i] == "."
            ):
                number = expression[i] + number
                i -= 1

            if not number:
                raise ValueError

            factorial_result = math.factorial(
                int(number)
            )

            expression = (
                expression[:i + 1]
                + str(factorial_result)
                + expression[index + 1:]
            )

        return expression

    # =============================
    # ERROR MESSAGE
    # =============================

    def show_error(self, message):

        self.display.delete(0, tk.END)
        self.display.insert(0, message)

        self.expression = ""

    # =============================
    # KEYBOARD SUPPORT
    # =============================

    def keyboard_input(self, event):

        key = event.keysym
        char = event.char

        if char in "0123456789.+-*/()":
            self.add_to_expression(char)

        elif key == "Return":
            self.calculate()

        elif key == "BackSpace":
            self.backspace()

        elif key == "Escape":
            self.clear()


# =================================
# APPLICATION ENTRY POINT
# =================================

if __name__ == "__main__":

    window = tk.Tk()

    app = SmartCalcPro(window)

    window.mainloop()