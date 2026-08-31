import tkinter as tk
window = tk.Tk()
window.title("SmartCalc Pro")
window.geometry("500x700")
window.resizable(False, False)


label = tk.Label(window, text="SmartCalc Pro", font=("Arial", 24))
label.pack(pady=20)
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

display = tk.Entry(window, font=("Arial", 24), justify="right")
display.pack(padx=20, pady=10, fill="x")

def add_to_display(value):
    display.insert(tk.END, value)

button_7 = tk.Button(button_frame, text="7", command=lambda: add_to_display("7"))
button_7.pack()

window.mainloop()
