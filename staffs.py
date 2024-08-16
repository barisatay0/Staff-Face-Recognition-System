import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk
import os
import subprocess
import shutil

# Function that starts the model training process
def run_trainer():
    try:
        subprocess.run(["python", "trainer.py"])
    except Exception as e:
        print(f"Error: {e}")

# Function that deletes the folder belonging to the specified staff id
def delete_staff_folder(staff_no):
    folder_path = os.path.join('Data', staff_no)
    if os.path.exists(folder_path):
        try:
            shutil.rmtree(folder_path)
            print(f"{staff_no} Staff is deleted.")
        except OSError as e:
            print(f"Error: {folder_path} Could not delete folder: {e}")
    else:
        print(f"{staff_no} Staff folder number could not be found.")

# Function that loads staff data
def load_data():
    try:
        df = pd.read_excel('data.xlsx')
        return df
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load file: {e}")
        return pd.DataFrame()

# Function that saves staff data
def save_data(df):
    try:
        df.to_excel('data.xlsx', index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Data could not be saved: {e}")

# Function that lists staff
def list_staffs():
    df = load_data()
    for row in tree.get_children():
        tree.delete(row)
    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Function that performs staff deletion
def delete_staff():
    df = load_data()
    staff_no = simpledialog.askstring("Input", "Staff id:")
    if staff_no:
        df = df[df['StaffId'].astype(str) != staff_no]
        save_data(df)
        list_staffs()
        delete_staff_folder(staff_no)
        run_trainer()

# Function that updates staff name and surname
def update_staff_name_surname(staff_no):
    df = load_data()
    new_name = simpledialog.askstring("Input", "New Staff Name:")
    new_surname = simpledialog.askstring("Input", "New Staff Surname:")
    df.loc[df['StaffId'].astype(str) == staff_no, 'Name'] = new_name
    df.loc[df['StaffId'].astype(str) == staff_no, 'Surname'] = new_surname
    save_data(df)
    list_staffs()

# Function that updates the staff number
def update_staff_number(staff_no):
    df = load_data()
    new_number = simpledialog.askstring("Input", "New Staff ID:")
    df.loc[df['StaffId'].astype(str) == staff_no, 'StaffId'] = new_number
    save_data(df)
    list_staffs()

# Main function that performs the staff update operation
def update_staff():
    staff_no = simpledialog.askstring("Input", "Staff id:")
    if staff_no:
        if staff_no in load_data()['StaffId'].astype(str).values:
            update_window = tk.Toplevel(root)
            update_window.title("Staff update options")

              # Name and Surname update button
            btn_name_surname = tk.Button(update_window, text="Update Name And Surname", 
                                         command=lambda: [update_staff_name_surname(staff_no), update_window.destroy()])
            btn_name_surname.pack(pady=10)

            # Staff number update button
            btn_number = tk.Button(update_window, text="Update Staff ID", 
                                   command=lambda: [update_staff_number(staff_no), update_window.destroy()])
            btn_number.pack(pady=10)
        else:
            messagebox.showerror("Error", "Staff Not Found")

# Creating the main window
root = tk.Tk()
root.iconbitmap("")
root.title("Staff Management")
root.geometry("800x400")
root.configure(bg="#f0f0f0")

# Frame where the buttons will be placed
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

# Styles of buttons
button_style = {
    "font": ("Arial", 12),
    "bg": "#0092A3",
    "fg": "white",
    "activebackground": "#056B76",
    "width": 20,
    "bd": 0,
    "relief": tk.FLAT,
    "padx": 5,
    "pady": 5
}

# Staff listing button
list_button = tk.Button(frame, text="List Staff", command=list_staffs, **button_style)
list_button.grid(row=0, column=0, padx=5, pady=5)

# Staff delete button
delete_button = tk.Button(frame, text="Delete Staff", command=delete_staff, **button_style)
delete_button.grid(row=0, column=1, padx=5, pady=5)

# Staff update button
update_button = tk.Button(frame, text="Update Staff", command=update_staff, **button_style)
update_button.grid(row=0, column=2, padx=5, pady=5)

# Table where staff will be displayed
columns = ["Name", "Surname", "StaffId", "Department", "Check"]
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Name", text="Name")
tree.heading("Surname", text="Surname")
tree.heading("StaffId", text="Staff id")
tree.heading("Department", text="Department")
tree.heading("Check", text="Check")

# Column widths of the table
for col in columns:
    tree.column(col, width=150)

tree.pack(pady=20)

# Start main loop
root.mainloop()
