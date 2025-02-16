import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json
import os

CONTACTS_FILE = "contacts.json"

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("610x510")  
        self.root.configure(bg="#f0f0f0") 

       
        print("Initializing contact book...")  

        try:
            self.bg_image = Image.open("Bg.jpg")
            self.bg_image = self.bg_image.resize((610, 510), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
            self.canvas = tk.Canvas(self.root, width=610, height=510)
            self.canvas.pack(fill="both", expand=True)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print("ALT")
            self.root.configure(bg="#d9d9d9")  

        
        self.contact_data = []
        self.contacts = self.load_contacts()

        
        self.create_interface()

    def create_interface(self):
        """Creates all UI elements for the Contact Book."""

        # Frame for contact entry
        self.frame = tk.Frame(self.root, bg="#ffffff", bd=4, relief=tk.RIDGE)
        self.frame.place(x=45, y=25, width=510, height=160)

        font_style = ("Arial", 13, "bold")

        
        print("Creating entry fields...")  

        # Labels & Entry Fields
        tk.Label(self.frame, text="Full Name:", font=font_style, bg="white").grid(row=0, column=0, padx=10, pady=3, sticky="w")
        self.name_entry = tk.Entry(self.frame, font=("Arial", 12), width=26, bd=2, relief=tk.SUNKEN)
        self.name_entry.grid(row=0, column=1, padx=10, pady=3)

        tk.Label(self.frame, text="Phone Number:", font=font_style, bg="white").grid(row=1, column=0, padx=10, pady=3, sticky="w")
        self.phone_entry = tk.Entry(self.frame, font=("Arial", 12), width=26, bd=2, relief=tk.SUNKEN)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=3)

        tk.Label(self.frame, text="Email Address:", font=font_style, bg="white").grid(row=2, column=0, padx=10, pady=3, sticky="w")
        self.email_entry = tk.Entry(self.frame, font=("Arial", 12), width=26, bd=2, relief=tk.SUNKEN)
        self.email_entry.grid(row=2, column=1, padx=10, pady=3)

        # Add Button
        self.add_button = tk.Button(self.frame, text="➕ Add Contact", command=self.add_contact, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_button.grid(row=3, column=0, columnspan=2, pady=8, ipadx=15, ipady=2)

        # Contact List Display
        self.list_frame = tk.Frame(self.root, bg="white")
        self.list_frame.place(x=45, y=200, width=510, height=250)

        self.contact_list = ttk.Treeview(self.list_frame, columns=("Name", "Phone", "Email"), show="headings")
        self.contact_list.heading("Name", text="Name")
        self.contact_list.heading("Phone", text="Phone")
        self.contact_list.heading("Email", text="Email")
        self.contact_list.column("Name", width=170)
        self.contact_list.column("Phone", width=130)
        self.contact_list.column("Email", width=180)
        self.contact_list.pack(fill="both", expand=True)

        self.contact_list.bind("<Double-1>", self.load_selected_contact)

        # Delete Button
        self.delete_button = tk.Button(self.root, text="❌ Delete", command=self.delete_contact, bg="red", fg="white", font=("Arial", 12))
        self.delete_button.place(x=45, y=460, width=160, height=30)

        self.refresh_list()

    def load_contacts(self):
        """Loads contacts from a JSON file."""
        if os.path.exists(CONTACTS_FILE):
            try:
                with open(CONTACTS_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("ErroR")
                return []
        return []

    def save_contacts(self):
        """Saves contacts to a JSON file."""
        with open(CONTACTS_FILE, "w") as file:
            json.dump(self.contacts, file, indent=4)

    def add_contact(self):
        """Adds a new contact (but forgot to handle duplicates)."""
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not phone or not email:
            messagebox.showwarning( "Please fill out all fields!")
            return

        
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.save_contacts()
        self.refresh_list()
        self.clear_entries()

    def refresh_list(self):
        """Refreshes the displayed contact list."""
        for row in self.contact_list.get_children():
            self.contact_list.delete(row)

        for contact in self.contacts:
            self.contact_list.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

    def clear_entries(self):
        """Clears input fields."""
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def load_selected_contact(self, event):
        """Loads a selected contact into the form for editing."""
        selected = self.contact_list.selection()
        if not selected:
            return

        item = self.contact_list.item(selected)
        name, phone, email = item["values"]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, name)

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, phone)

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, email)

    def delete_contact(self):
        """Deletes a selected contact."""
        selected = self.contact_list.selection()
        if not selected:
            messagebox.showwarning("Delete Error", "No contact selected!")
            return

        item = self.contact_list.item(selected)
        name = item["values"][0]

        self.contacts = [contact for contact in self.contacts if contact["name"] != name]
        self.save_contacts()
        self.refresh_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
