# ============================================================
# PROJECT 9: Simple Calculator (Tkinter GUI)
# ============================================================

import tkinter as tk
from math import sqrt, pi, e, log, sin, cos, tan, radians

class SimpleCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.resizable(False, False)
        self.expression = ""
        self.history = []
        self.build_ui()

    def build_ui(self):
        self.root.configure(bg="#2D2D2D")

        # Display
        display_frame = tk.Frame(self.root, bg="#2D2D2D")
        display_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

        self.history_display = tk.Label(display_frame, text="",
                                         font=("Courier New", 11),
                                         bg="#2D2D2D", fg="#888888",
                                         anchor="e", width=30)
        self.history_display.pack(fill=tk.X)

        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(display_frame, textvariable=self.display_var,
                                 font=("Courier New", 32, "bold"),
                                 bg="#1C1C1C", fg="#00FF41",
                                 bd=0, justify=tk.RIGHT,
                                 insertbackground="#00FF41",
                                 state="readonly", readonlybackground="#1C1C1C")
        self.display.pack(fill=tk.X, ipady=8)

        # Button layout: (text, row, col, colspan, color)
        buttons = [
            # Row 1 - functions
            ("C",    1, 0, 1, "#FF6B6B"), ("⌫",   1, 1, 1, "#FF6B6B"),
            ("%",    1, 2, 1, "#4ECDC4"), ("÷",   1, 3, 1, "#45B7D1"),
            ("√",    1, 4, 1, "#A29BFE"),
            # Row 2
            ("7",    2, 0, 1, "#333333"), ("8",   2, 1, 1, "#333333"),
            ("9",    2, 2, 1, "#333333"), ("×",   2, 3, 1, "#45B7D1"),
            ("x²",   2, 4, 1, "#A29BFE"),
            # Row 3
            ("4",    3, 0, 1, "#333333"), ("5",   3, 1, 1, "#333333"),
            ("6",    3, 2, 1, "#333333"), ("−",   3, 3, 1, "#45B7D1"),
            ("1/x",  3, 4, 1, "#A29BFE"),
            # Row 4
            ("1",    4, 0, 1, "#333333"), ("2",   4, 1, 1, "#333333"),
            ("3",    4, 2, 1, "#333333"), ("+",   4, 3, 1, "#45B7D1"),
            ("±",    4, 4, 1, "#A29BFE"),
            # Row 5
            ("0",    5, 0, 2, "#333333"), (".",   5, 2, 1, "#333333"),
            ("=",    5, 3, 2, "#00B894"),
        ]

        self.btn_widgets = {}
        for (text, row, col, span, color) in buttons:
            btn = tk.Button(self.root, text=text,
                             font=("Arial", 16, "bold"),
                             bg=color, fg="white",
                             activebackground="#555",
                             activeforeground="white",
                             relief=tk.FLAT, bd=1,
                             command=lambda t=text: self.on_click(t))
            btn.grid(row=row, column=col, columnspan=span,
                      padx=3, pady=3, sticky="nsew", ipady=12)
            self.btn_widgets[text] = btn

        for i in range(6):
            self.root.rowconfigure(i, weight=1)
        for i in range(5):
            self.root.columnconfigure(i, weight=1)

        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        key = event.char
        if key in "0123456789.":
            self.on_click(key)
        elif key in "+-*/":
            ops = {'+': '+', '-': '−', '*': '×', '/': '÷'}
            self.on_click(ops.get(key, key))
        elif key in ('\r', '='):
            self.on_click('=')
        elif key == '\x08':
            self.on_click('⌫')

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
            self.display_var.set("0")
            self.history_display.config(text="")

        elif char == '⌫':
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression or "0")

        elif char == '=':
            try:
                expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
                result = eval(expr)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                self.history_display.config(text=f"{self.expression} =")
                self.history.append(f"{self.expression} = {result}")
                self.expression = str(result)
                self.display_var.set(result)
            except Exception:
                self.display_var.set("Error")
                self.expression = ""

        elif char == '√':
            try:
                val = float(eval(self.expression.replace('×','*').replace('÷','/').replace('−','-')))
                result = sqrt(val)
                if result.is_integer(): result = int(result)
                self.history_display.config(text=f"√({self.expression}) =")
                self.expression = str(result)
                self.display_var.set(result)
            except:
                self.display_var.set("Error")
                self.expression = ""

        elif char == 'x²':
            try:
                val = float(eval(self.expression.replace('×','*').replace('÷','/').replace('−','-')))
                result = val ** 2
                if isinstance(result, float) and result.is_integer(): result = int(result)
                self.history_display.config(text=f"({self.expression})² =")
                self.expression = str(result)
                self.display_var.set(result)
            except:
                self.display_var.set("Error")
                self.expression = ""

        elif char == '1/x':
            try:
                val = float(eval(self.expression.replace('×','*').replace('÷','/').replace('−','-')))
                result = 1 / val
                self.history_display.config(text=f"1/({self.expression}) =")
                self.expression = str(result)
                self.display_var.set(result)
            except:
                self.display_var.set("Error")
                self.expression = ""

        elif char == '±':
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.display_var.set(self.expression)

        elif char == '%':
            try:
                val = float(eval(self.expression.replace('×','*').replace('÷','/').replace('−','-')))
                result = val / 100
                self.expression = str(result)
                self.display_var.set(result)
            except:
                self.display_var.set("Error")
                self.expression = ""

        else:
            self.expression += char
            self.display_var.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCalculator(root)
    root.mainloop()
