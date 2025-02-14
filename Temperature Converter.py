import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Parent Class: General Converter
class Converter:
    def __init__(self):
        pass  # Can be extended for other conversion types

    def convert(self, value):
        raise NotImplementedError("Subclasses must implement conversion logic")
# Child Class (Temperature converter)
class TemperatureConverter(Converter):
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Converter")

        # Label and Entry for temperature input
        self.label = tk.Label(root, text="Enter Temperature:")
        self.label.pack(pady=5)

        self.temp_entry = tk.Entry(root)
        self.temp_entry.pack(pady=5)

        # Conversion option
        self.var = tk.StringVar(value="F to C")
        self.radio1 = tk.Radiobutton(root, text="Fahrenheit to Celsius", variable=self.var, value="F to C")
        self.radio2 = tk.Radiobutton(root, text="Celsius to Fahrenheit", variable=self.var, value="C to F")
        self.radio1.pack()
        self.radio2.pack()

        # Convert Button
        self.convert_button = tk.Button(root, text="Convert", command=self.convert_temperature)
        self.convert_button.pack(pady=10)

        # Label to display result
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=5)

    def convert_temperature(self):
        try:
            temp = float(self.temp_entry.get())
            if self.var.get() == "F to C":
                converted_temp = (temp - 32) * 5 / 9
                conversion_text = f"{temp}°F = {converted_temp:.2f}°C"
            else:
                converted_temp = (temp * 9 / 5) + 32
                conversion_text = f"{temp}°C = {converted_temp:.2f}°F"

            self.result_label.config(text=conversion_text)
            self.plot_temperature(temp, converted_temp)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")

    def plot_temperature(self, original, converted):
        # Create a bar chart to compare temperatures
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(["Original", "Converted"], [original, converted], color=['blue', 'red'])
        ax.set_ylabel("Temperature")
        ax.set_title("Temperature Conversion")

        # Embed the plot into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureConverter(root)
    root.mainloop()
