import tkinter as tk
from tkinter import messagebox


class TemperatureConverter:
    def __init__(self, root):
        self.root = root
        self.root.geometry('350x150')
        self.root.title('Temperature Converter')

        # Variables
        self.input_var = tk.StringVar()
        self.unit_var = tk.StringVar(value="Celsius")

        self.create_widgets()
        self.setup_grid_resizing()

    def create_widgets(self):
        """Creates the UI components."""
        tk.Label(self.root, text="Enter Temperature:").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.entry = tk.Entry(self.root, textvariable=self.input_var)
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.entry.bind("<Return>", lambda event: self.convert())  # Press Enter to convert

        tk.OptionMenu(self.root, self.unit_var, "Celsius", "Fahrenheit").grid(row=0, column=2, padx=10, pady=10)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.result_label.grid(row=2, column=0, columnspan=3, pady=10)

        convert_button = tk.Button(self.root, text="Convert", command=self.convert)
        convert_button.grid(row=1, column=0, columnspan=3, pady=10, sticky="ew")

    def setup_grid_resizing(self):
        """Configures grid for better UI resizing."""
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def convert(self):
        """Converts the temperature between Celsius and Fahrenheit."""
        try:
            temp = float(self.input_var.get().strip())  # Remove spaces & convert input
            unit = self.unit_var.get()

            if unit == "Celsius":
                result = (temp * 9 / 5) + 32
                self.result_label.config(text=f"{result:.1f} °F")
            else:
                result = (temp - 32) * 5 / 9
                self.result_label.config(text=f"{result:.1f} °C")

        except ValueError:
            self.result_label.config(text="Invalid input!")
            messagebox.showerror("Input Error", "Please enter a valid number.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureConverter(root)
    root.mainloop()
