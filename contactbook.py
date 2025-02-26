import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("800x600")
        
        # Database Connection
        self.conn = sqlite3.connect('contacts.db')
        self.create_table()
        
        # Variables for form fields
        self.id_var = tk.StringVar() 
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.search_var = tk.StringVar()
        
        # Background Image
        self.set_background()
        
        # Create Widgets
        self.create_widgets()
        
        # Load initial data
        self.fetch_data()
    
    def set_background(self):
        try:
            # Try to load the image if it exists
            self.bg_image = Image.open("Bg.jpg")
            self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((800, 600), Image.LANCZOS))
            self.bg_label = tk.Label(self.root, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            # If image doesn't exist, use a solid color
            self.root.configure(bg="#f0f0f0")
            messagebox.showinfo("Background Image", "No background image found. Using default color.")
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT
            )'''
        )
        self.conn.commit()
    
    def create_widgets(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg='white', bd=5, relief=tk.RIDGE)
        main_frame.place(x=20, y=20, width=760, height=560)
        
        # Title
        title_label = tk.Label(main_frame, text="Contact Management System", 
                               font=("times new roman", 18, "bold"), bg="white", fg="navy blue")
        title_label.pack(side=tk.TOP, fill=tk.X)
        
        # Left Frame for input fields
        left_frame = tk.LabelFrame(main_frame, text="Contact Details", bg="white",
                                  font=("times new roman", 12, "bold"), fg="navy blue", bd=4, relief=tk.RIDGE)
        left_frame.place(x=20, y=50, width=330, height=480)
        
        # Input fields
        # Name
        lbl_name = tk.Label(left_frame, text="Name:", bg="white", font=("times new roman", 12, "bold"))
        lbl_name.grid(row=0, column=0, padx=10, pady=20, sticky="w")
        
        entry_name = tk.Entry(left_frame, textvariable=self.name_var, font=("times new roman", 12), width=15)
        entry_name.grid(row=0, column=1, padx=10, pady=20, sticky="w")
        
        # Phone
        lbl_phone = tk.Label(left_frame, text="Phone:", bg="white", font=("times new roman", 12, "bold"))
        lbl_phone.grid(row=1, column=0, padx=10, pady=20, sticky="w")
        
        entry_phone = tk.Entry(left_frame, textvariable=self.phone_var, font=("times new roman", 12), width=15)
        entry_phone.grid(row=1, column=1, padx=10, pady=20, sticky="w")
        
        # Email
        lbl_email = tk.Label(left_frame, text="Email:", bg="white", font=("times new roman", 12, "bold"))
        lbl_email.grid(row=2, column=0, padx=10, pady=20, sticky="w")
        
        entry_email = tk.Entry(left_frame, textvariable=self.email_var, font=("times new roman", 12), width=15)
        entry_email.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        
        # Button Frame
        btn_frame = tk.Frame(left_frame, bg="white", bd=2, relief=tk.RIDGE)
        btn_frame.place(x=10, y=320, width=290, height=100)
        
        # Buttons
        add_btn = tk.Button(btn_frame, text="Add", command=self.add_data, width=8, font=("times new roman", 10, "bold"), bg="green", fg="white")
        add_btn.grid(row=0, column=0, padx=10, pady=20)
        
        update_btn = tk.Button(btn_frame, text="Update", command=self.update_data, width=8, font=("times new roman", 10, "bold"), bg="blue", fg="white")
        update_btn.grid(row=0, column=1, padx=10, pady=20)
        
        delete_btn = tk.Button(btn_frame, text="Delete", command=self.delete_data, width=8, font=("times new roman", 10, "bold"), bg="red", fg="white")
        delete_btn.grid(row=0, column=2, padx=10, pady=20)
        
        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear, width=8, font=("times new roman", 10, "bold"), bg="orange", fg="white")
        clear_btn.grid(row=1, column=1, padx=10, pady=20)
        
        # Right Frame for displaying data
        right_frame = tk.LabelFrame(main_frame, text="Contact List", bg="white",
                                   font=("times new roman", 12, "bold"), fg="navy blue", bd=4, relief=tk.RIDGE)
        right_frame.place(x=370, y=50, width=370, height=480)
        
        # Search Frame
        search_frame = tk.Frame(right_frame, bg="white", bd=2, relief=tk.RIDGE)
        search_frame.place(x=10, y=10, width=350, height=60)
        
        lbl_search = tk.Label(search_frame, text="Search By Name:", bg="white", font=("times new roman", 11, "bold"))
        lbl_search.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        
        entry_search = tk.Entry(search_frame, textvariable=self.search_var, font=("times new roman", 11), width=15)
        entry_search.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        
        search_btn = tk.Button(search_frame, text="Search", command=self.search_data, width=6, font=("times new roman", 10, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=2, padx=5, pady=10)
        
        show_all_btn = tk.Button(search_frame, text="Show All", command=self.fetch_data, width=6, font=("times new roman", 10, "bold"), bg="green", fg="white")
        show_all_btn.grid(row=0, column=3, padx=5, pady=10)
        
        # Table Frame
        table_frame = tk.Frame(right_frame, bd=2, relief=tk.RIDGE, bg="white")
        table_frame.place(x=10, y=80, width=350, height=370)
        
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        
        self.contact_table = ttk.Treeview(table_frame, columns=("id", "name", "phone", "email"),
                                         xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x.config(command=self.contact_table.xview)
        scroll_y.config(command=self.contact_table.yview)
        
        self.contact_table.heading("id", text="ID")
        self.contact_table.heading("name", text="Name")
        self.contact_table.heading("phone", text="Phone")
        self.contact_table.heading("email", text="Email")
        
        self.contact_table['show'] = 'headings'
        
        self.contact_table.column("id", width=30)
        self.contact_table.column("name", width=100)
        self.contact_table.column("phone", width=100)
        self.contact_table.column("email", width=100)
        
        self.contact_table.pack(fill=tk.BOTH, expand=1)
        
        # Bind the table for row selection
        self.contact_table.bind("<ButtonRelease-1>", self.get_cursor)
    
    def add_data(self):
        if self.name_var.get() == "":
            messagebox.showerror("Error", "Name is required")
        else:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)",
                    (
                        self.name_var.get(),
                        self.phone_var.get(),
                        self.email_var.get(),
                    )
                )
                self.conn.commit()
                self.fetch_data()
                self.clear()
                messagebox.showinfo("Success", "Contact added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding contact: {str(e)}")
    
    def fetch_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contacts")
            rows = cursor.fetchall()
            
            if len(rows) > 0:
                self.contact_table.delete(*self.contact_table.get_children())
                for row in rows:
                    self.contact_table.insert('', tk.END, values=row)
                    
            self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {str(e)}")
    
    def get_cursor(self, event=""):
        try:
            cursor_row = self.contact_table.focus()
            content = self.contact_table.item(cursor_row)
            row = content['values']
            
            if len(row) > 0:
                self.id_var.set(row[0])
                self.name_var.set(row[1])
                self.phone_var.set(row[2])
                self.email_var.set(row[3])
        except Exception as e:
            pass
    
    def update_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select a contact to update")
        else:
            try:
                cursor = self.conn.cursor()
                cursor.execute(
                    "UPDATE contacts SET name=?, phone=?, email=? WHERE id=?",
                    (
                        self.name_var.get(),
                        self.phone_var.get(),
                        self.email_var.get(),
                        self.id_var.get(),
                    )
                )
                self.conn.commit()
                self.fetch_data()
                self.clear()
                messagebox.showinfo("Success", "Contact updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error updating contact: {str(e)}")
    
    def delete_data(self):
        if self.id_var.get() == "":
            messagebox.showerror("Error", "Select a contact to delete")
        else:
            try:
                confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this contact?")
                if confirm:
                    cursor = self.conn.cursor()
                    cursor.execute("DELETE FROM contacts WHERE id=?", (self.id_var.get(),))
                    self.conn.commit()
                    self.fetch_data()
                    self.clear()
                    messagebox.showinfo("Success", "Contact deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting contact: {str(e)}")
    
    def clear(self):
        self.id_var.set("")
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
    
    def search_data(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM contacts WHERE name LIKE ?", ('%' + self.search_var.get() + '%',))
            rows = cursor.fetchall()
            
            if len(rows) > 0:
                self.contact_table.delete(*self.contact_table.get_children())
                for row in rows:
                    self.contact_table.insert('', tk.END, values=row)
                
                self.conn.commit()
            else:
                messagebox.showinfo("Info", "No matching records found")
                self.fetch_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {str(e)}")
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
