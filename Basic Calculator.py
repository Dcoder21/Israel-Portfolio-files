import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.expression = ""  # Holds the current calculation expression

        # Create a display Entry widget (read-only)
        self.display = tk.Entry(root, font=("Segoe UI", 24), bd=10, relief=tk.RIDGE, justify="right")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipady=10)
        
        # Define button texts and their grid positions
        buttons = [
            ("C", 1, 0), ("X", 1, 1), ("%", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2)
        ]

        # Create buttons using grid layout
        for (text, row, col) in buttons:
            # The "=" button spans two columns
            if text == "=":
                button = tk.Button(root, text=text, font=("Segoe UI", 24), bd=5, relief=tk.RIDGE,
                                   bg="#4caf50", fg="white", command=self.evaluate)
                button.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=5, pady=5)
            else:
                button = tk.Button(root, text=text, font=("Segoe UI", 24), bd=5, relief=tk.RIDGE,
                                   command=lambda txt=text: self.on_button_click(txt))
                button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weights for even resizing (optional if window size is fixed)
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        for j in range(4):
            self.root.grid_columnconfigure(j, weight=1)

    def on_button_click(self, char):
        """Handle button clicks to update the expression or perform operations."""
        if char == "C":
            # Clear the entire expression
            self.expression = ""
            self.display.delete(0, tk.END)
        elif char == "X":
            # Remove the last character (backspace)
            self.expression = self.expression[:-1]
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)
        else:
            # Append the pressed button's text to the expression
            self.expression += str(char)
            self.display.delete(0, tk.END)
            self.display.insert(0, self.expression)

    def evaluate(self):
        """Evaluate the current expression and display the result."""
        try:
            # Evaluate the arithmetic expression and update the display
            result = str(eval(self.expression))
            self.display.delete(0, tk.END)
            self.display.insert(0, result)
            self.expression = result
        except Exception:
            messagebox.showerror("Error", "Invalid Expression")
            self.expression = ""
            self.display.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
