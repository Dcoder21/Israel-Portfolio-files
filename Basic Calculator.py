import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Handmade Calculator")
        self.root.geometry("320x430")  
        self.root.configure(bg="#ddd")
        self.expression = ""  
        self.last_result = None  

        # Display for input/output
        self.display = tk.Entry(root, font=("Arial", 20), bd=8, relief=tk.SUNKEN, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, ipadx=8, ipady=8, padx=5, pady=5, sticky="nsew")

        
        self.create_buttons()

        # Keyboard support
        self.root.bind("<Key>", self.handle_key)

    def create_buttons(self):
     
        
        # First row (Clear, Backspace, %, /)
        tk.Button(self.root, text="C", font=("Arial", 18), command=lambda: self.button_click("C")).grid(row=1, column=0, ipadx=15, ipady=10, sticky="nsew")
        tk.Button(self.root, text="←", font=("Arial", 18), command=lambda: self.button_click("←")).grid(row=1, column=1, ipadx=15, ipady=10, sticky="nsew")
        tk.Button(self.root, text="%", font=("Arial", 18), command=lambda: self.button_click("%")).grid(row=1, column=2, ipadx=15, ipady=10, sticky="nsew")
        tk.Button(self.root, text="/", font=("Arial", 18), command=lambda: self.button_click("/")).grid(row=1, column=3, ipadx=15, ipady=10, sticky="nsew")  

        # Numeric keys and operators
        nums = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1)
        ]
        for text, row, col in nums:
            tk.Button(self.root, text=text, font=("Arial", 18), command=lambda t=text: self.button_click(t)).grid(row=row, column=col, ipadx=15, ipady=10, sticky="nsew")

        
        tk.Button(self.root, text="=", font=("Arial", 18), bg="#4CAF50", fg="white", command=self.calculate).grid(row=5, column=2, columnspan=2, ipadx=30, ipady=10, sticky="nsew")
        tk.Button(self.root, text="Ans", font=("Arial", 15), command=self.insert_ans).grid(row=6, column=0, columnspan=4, ipadx=20, ipady=5, sticky="nsew")

    def button_click(self, char):
        """Handles button clicks, including clear and backspace."""
        print(f"DEBUG: Button pressed: {char}")  

        if char == "C":
            self.expression = ""
        elif char == "←":
            self.expression = self.expression[:-1]
        else:
            self.expression += char

        self.update_display()

    def update_display(self):
        """Updates the calculator display."""
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def calculate(self):
        
        try:
            result = self.manual_eval(self.expression)
            print(f"DEBUG: Calculation result: {result}")  
            self.last_result = result  
            self.expression = str(result)
        except Exception:
            self.expression = "Error"
        
        self.update_display()

    def manual_eval(self, expression):
    
        try:
            tokens = list(expression)
            result = 0
            num = ""
            operator = "+"

            for char in tokens:
                if char.isdigit() or char == ".":
                    num += char
                else:
                    if num:
                        if operator == "+":
                            result += float(num)
                        elif operator == "-":
                            result -= float(num)
                        elif operator == "*":
                            result *= float(num)  
                        elif operator == "/":
                            try:
                                result /= float(num) if float(num) != 0 else 1  
                            except:
                                return "Error"
                        num = ""
                    operator = char  

            if num:
                if operator == "+":
                    result += float(num)
                elif operator == "-":
                    result -= float(num)
                elif operator == "*":
                    result *= float(num)
                elif operator == "/":
                    result /= float(num) if float(num) != 0 else 1

            return result
        except:
            return "Error"

    def insert_ans(self):
        
        if self.last_result is not None:
            self.expression += str(self.last_result)
            self.update_display()

    def handle_key(self, event):
        """Handles keyboard input."""
        if event.char in "0123456789+-*/.%":
            self.button_click(event.char)
        elif event.keysym == "Return":
            self.calculate()
        elif event.keysym == "BackSpace":
            self.button_click("←")

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
