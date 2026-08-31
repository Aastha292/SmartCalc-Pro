import tkinter as tk
import math
from smart_assistant import SmartAssistant
from calculation_engine import CalculationEngine, CalculationError
from storage import CalculatorStorage

class SmartCalcPro:
    def __init__(self, window):
        self.window = window

        # -----------------------------
        # Window configuration
        # -----------------------------
        self.window.title("SmartCalc Pro")
        self.window.geometry("500x760")
        self.window.resizable(False, False)
        self.window.configure(bg="#0F172A")

        # -----------------------------
        # Calculator state
        # -----------------------------
        self.expression = ""
        self.storage = CalculatorStorage()
        self.history, self.memory = self.storage.load()
        self.last_answer = 0
        self.angle_mode = "DEG"
        self.assistant = SmartAssistant()
        self.engine = CalculationEngine()
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        # -----------------------------
        # Build interface
        # -----------------------------
        self.create_header()
        self.create_display()
        self.create_smart_assistant()
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
        header.pack(fill="x", padx=20, pady=(18, 12))

        title = tk.Label(
            header,
            text="SmartCalc Pro",
            font=("Segoe UI", 26, "bold"),
            bg="#111827",
            fg="white"
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="Advanced Scientific Calculator",
            font=("Segoe UI", 10, "normal"),
            bg="#111827",
            fg="#9CA3AF"
        )
        subtitle.pack(pady=(3, 0))
        history_button = tk.Button(
            header,
            text="🕘 History",
            font=("Segoe UI", 9, "bold"),
            bg="#374151",
            fg="white",
            activebackground="#4B5563",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=14,
            pady=6,
            command=self.show_history
            )

        history_button.pack(pady=(8, 0))

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
            font=("Segoe UI", 28, "bold"),
            justify="right",
            bg="#F8FAFC",
            fg="#0F172A",
            insertbackground="#2563EB",
            relief="flat",
            bd=0
        )

        self.display.pack(
            fill="x",
            padx=15,
            pady=22
        )
        self.status_var = tk.StringVar(value="Ready • Scientific Mode")

        status = tk.Label(
            self.window,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            bg="#0F172A",
            fg="#94A3B8"
        )
        status.pack(
            anchor="e",
            padx=25,
            pady=(0, 5)
        )

    # =============================
    # SMART ASSISTANT
    # =============================

    def create_smart_assistant(self):

        assistant_frame = tk.Frame(
            self.window,
            bg="#E5E7EB"
        )
        assistant_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 10)
        )

        assistant_title = tk.Label(
            assistant_frame,
            text="🧠 Smart Assistant",
            font=("Segoe UI", 12, "bold"),
            bg="#E5E7EB",
            fg="#111827"
        )
        assistant_title.pack(
            anchor="w",
            padx=12,
            pady=(10, 2)
        )

        assistant_hint = tk.Label(
            assistant_frame,
            text="Ask a math question or enter a smart calculation",
            font=("Segoe UI", 9),
            bg="#E5E7EB",
            fg="#6B7280"
        )
        assistant_hint.pack(
            anchor="w",
            padx=12,
            pady=(0, 6)
        )

        input_frame = tk.Frame(
            assistant_frame,
            bg="#E5E7EB"
        )
        input_frame.pack(
            fill="x",
            padx=12,
            pady=(0, 10)
        )

        self.assistant_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            relief="flat",
            bd=0
        )
        self.assistant_entry.bind("<Return>", lambda event: self.smart_solve())
        self.assistant_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=8
        )

        solve_button = tk.Button(
            input_frame,
            text="SOLVE",
            font=("Segoe UI", 9, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=7,
            command=self.smart_solve
        )
        solve_button.pack(
            side="left",
            padx=(8, 0)
        )

        self.assistant_result = tk.Label(
            assistant_frame,
            text="",
            font=("Segoe UI", 10),
            bg="#E5E7EB",
            fg="#111827",
            justify="left",
            anchor="w"
        )
        self.assistant_result.pack(
            fill="x",
            padx=12,
            pady=(0, 10)
        )

    def smart_solve(self):

        query = self.assistant_entry.get()

        result = self.assistant.solve(query)

        self.assistant_result.config(
            text=result
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
            pady=8
        )

        buttons = [
            ["MC", "MR", "M+", "M−"],
            ["DEG", "ANS", "C", "="],
            ["(", ")", "⌫", "sin"],
            ["cos", "tan", "√", "log"],
            ["ln", "x²", "xʸ", "π"],
            ["e", "7", "8", "9"],
            ["÷", "4", "5", "6"],
            ["×", "1", "2", "3"],
            ["−", "0", ".", "%"],
            ["+", "!", "", ""]
         ]

        for row, button_row in enumerate(buttons):
            button_frame.rowconfigure(row, weight=1)

            for column, text in enumerate(button_row):
                button_frame.columnconfigure(column, weight=1)

                button = tk.Button(
                    button_frame,
                    text=text,
                    font=("Segoe UI", 11, "bold"),
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda value=text: self.button_click(value)
                )

                button.grid(
                    row=row,
                    column=column,
                    sticky="nsew",
                    padx=2,
                    pady=2
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

        elif text in ["C", "⌫", "MC"]:
            button.configure(
                bg="#DC2626",
                fg="white",
                activebackground="#B91C1C",
                activeforeground="white"
            )

        elif text in [
            "sin", "cos", "tan", "√",
            "log", "ln", "x²", "xʸ",
            "π", "e", "!",
            "MR", "M+", "M−"
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

        if not value:
            return

        if value == "C":
            self.clear()

        elif value == "⌫":
            self.backspace()

        elif value == "=":
            self.calculate()

        elif value == "MC":
            self.memory = 0
            self.storage.save(self.history, self.memory)

        elif value == "MR":
            self.expression = str(self.memory)
            self.update_display()

        elif value == "M+":
            self.memory += self.get_current_value()
            self.storage.save(self.history, self.memory)

        elif value == "M−":
            self.memory -= self.get_current_value()
            self.storage.save(self.history, self.memory)
  
        elif value == "ANS":
            self.add_to_expression(str(self.last_answer))

        elif value == "DEG":
            self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
            self.status_var.set(f"Ready • {self.angle_mode} Mode")

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

    def get_current_value(self):
        try:
            return self.engine.evaluate(self.expression, self.angle_mode)
        except CalculationError:
            return 0

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
            result = self.engine.evaluate(self.expression, self.angle_mode)

            self.history.append(
                f"{self.expression} = {result}"
            )
            self.last_answer = result
            self.expression = str(result)
            self.update_display()
            self.storage.save(self.history, self.memory)

        except ZeroDivisionError:
            self.show_error("Cannot divide by zero.")

        except ValueError:
            self.show_error("Invalid mathematical value.")

        except CalculationError:
            self.show_error("Invalid expression.")

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

            if "." in number:
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
    # HISTORY WINDOW
    # =============================

    def show_history(self):

        history_window = tk.Toplevel(self.window)
        history_window.title("Calculation History")
        history_window.geometry("400x500")
        history_window.resizable(False, False)
        history_window.configure(bg="#111827")

        title = tk.Label(
            history_window,
            text="🕘 Calculation History",
            font=("Segoe UI", 18, "bold"),
            bg="#111827",
            fg="white"
        )
        title.pack(pady=(20, 10))

        history_list = tk.Listbox(
            history_window,
            font=("Consolas", 11),
            bg="white",
            fg="#111827",
            relief="flat",
            bd=0
        ) 
        history_list.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        if self.history:
            for item in self.history:
                history_list.insert(tk.END, item)
        else:
            history_list.insert(
                tk.END,
            "No calculations yet."
            )
        def clear_history():
            self.history.clear()
            self.storage.save(self.history, self.memory)
            history_list.delete(0, tk.END)
            history_list.insert(tk.END, "No calculations yet.")

        clear_button = tk.Button(
            history_window,
            text="Clear History",
            font=("Segoe UI", 10, "bold"),
            bg="#DC2626",
            fg="white",
            activebackground="#B91C1C",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2",
            command=clear_history
        )
        clear_button.pack(pady=(5, 5))

        close_button = tk.Button(
            history_window,
            text="Close",
            font=("Segoe UI", 10, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=20,
            pady=8,
            cursor="hand2",
            command=history_window.destroy
        )
        close_button.pack(pady=(5, 20))

    

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

    def close(self):
        self.storage.save(self.history, self.memory)
        self.window.destroy()


# =================================
# APPLICATION ENTRY POINT
# =================================

if __name__ == "__main__":

    window = tk.Tk()

    app = SmartCalcPro(window)

    window.mainloop()