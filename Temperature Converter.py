import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def convert_temperature():
    try:
        temp = float(entry.get())
        conversion_type = conversion_var.get()
        
        if conversion_type == "F to C":
            converted = (temp - 32) * 5 / 9
        else:
            converted = (temp * 9 / 5) + 32
        
        result_label.config(text=f"Converted: {converted:.2f}°")
        global last_conversion
        last_conversion = (temp, converted)
    except ValueError:
        messagebox.showerror("Error", "Enter a valid number.")

def show_graph():
    if "last_conversion" in globals():
        temp, converted = last_conversion
        plt.bar(["Original", "Converted"], [temp, converted], color=['blue', 'red'])
        plt.ylabel("Temperature")
        plt.title("Temperature Conversion")
        plt.show()
    else:
        messagebox.showinfo("Info", "Convert a temperature first.")

# Create GUI
temp = tk.Tk()
temp.title("Temperature Converter")

tk.Label(temp, text="Enter Temperature:", font=("Arial", 12)).pack()
entry = tk.Entry(temp)
entry.pack()

conversion_var = tk.StringVar(value="F to C")
tk.OptionMenu(root, conversion_var, "F to C", "C to F").pack()

tk.Button(temp, text="Convert", command=convert_temperature).pack()
result_label = tk.Label(temp, text="", font=("Arial", 14, "bold"))
result_label.pack()

tk.Button(temp, text="Show Graph", command=show_graph).pack()

root.mainloop()
