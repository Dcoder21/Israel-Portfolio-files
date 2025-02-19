import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class TemperatureConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Temperature Converter")
        
        self.last_conversion = None
        
        tk.Label(master, text="Enter Temperature:", font=("Arial", 12)).pack()
        self.entry = tk.Entry(master)
        self.entry.pack()
        
        self.conversion_var = tk.StringVar(value="F to C")
        tk.OptionMenu(master, self.conversion_var, "F to C", "C to F", "C to K", "K to C", "F to K", "K to F").pack()
        
        tk.Button(master, text="Convert", command=self.convert_temperature).pack()
        self.result_label = tk.Label(master, text="", font=("Arial", 14, "bold"))
        self.result_label.pack()
        
        tk.Button(master, text="Show Graph", command=self.show_graph).pack()
    
    def convert_temperature(self):
        try:
            temp = float(self.entry.get())
            conversion_type = self.conversion_var.get()
            
            if conversion_type == "F to C":
                converted = (temp - 32) * 5 / 9
            elif conversion_type == "C to F":
                converted = (temp * 9 / 5) + 32
            elif conversion_type == "C to K":
                converted = temp + 273.15
            elif conversion_type == "K to C":
                converted = temp - 273.15
            elif conversion_type == "F to K":
                converted = (temp - 32) * 5 / 9 + 273.15
            elif conversion_type == "K to F":
                converted = (temp - 273.15) * 9 / 5 + 32
            
            self.result_label.config(text=f"Converted: {converted:.2f}°")
            self.last_conversion = (temp, converted)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number.")
    
    def show_graph(self):
        if self.last_conversion:
            temp, converted = self.last_conversion
            plt.bar(["Original", "Converted"], [temp, converted], color=['blue', 'red'])
            plt.ylabel("Temperature")
            plt.title("Temperature Conversion")
            plt.show()
        else:
            messagebox.showinfo("Info", "Convert a temperature first.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperatureConverter(root)
    root.mainloop()
