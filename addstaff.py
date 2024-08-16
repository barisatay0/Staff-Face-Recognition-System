import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import openpyxl
import os
import cv2
import uuid
import subprocess

staffs = []

# Function to create Excel file
def create_excel_file():
    if not os.path.exists('data.xlsx'):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Staff"
        sheet.append(["Name", "Surname", "StaffId", "Department", "Check"])
        workbook.save("data.xlsx")

# Function of saving the staff to Excel file
def save_to_excel(staff):
    workbook = openpyxl.load_workbook("data.xlsx")
    sheet = workbook.active
    sheet.append([staff['name'], staff['surname'], staff['staff_id'], staff['class'], 0])
    workbook.save("data.xlsx")

# Folder creation function for staff
def create_staff_folder(staff_id):
    folder_path = os.path.join("Data", staff_id)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Photo taking function
def take_photos(staff_id):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Cam Error", "Camera is not available!")
        return False

    folder_path = create_staff_folder(staff_id)
    instructions = [
        "You can take photo with C Cheese!",
        "Come Closer!",
        "Left!",
        "Right!",
        "Up!",
        "Down!"
    ]

  # Photo taking cycle
    for instruction in instructions:
        messagebox.showinfo("Photo For AI", instruction)
        
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Cam Error", "We cant take a picture!")
            cap.release()
            cv2.destroyAllWindows()
            return False

        cv2.imshow("Photo For AI", frame)
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('c'):
                file_path = os.path.join(folder_path, f"{uuid.uuid4()}.png")
                cv2.imwrite(file_path, frame)
                break
            elif key == 27:  # If the escape key is pressed, close the window and cancel the operation
                cap.release()
                cv2.destroyAllWindows()
                return False

    cap.release()
    cv2.destroyAllWindows()
    return True

# Staff registration function
def save_staff():
    name = name_entry.get()
    surname = surname_entry.get()
    staff_id = id_entry.get()
    staff_class = class_combobox.get()
    if name and surname and staff_id and staff_class:
        staff = {'name': name, 'surname': surname, 'staff_id': staff_id, 'class': staff_class}
        if take_photos(staff_id):
            staffs.append(staff)
            save_to_excel(staff)
            create_staff_folder(staff_id)
            messagebox.showinfo("Success", "staff added successfully!")
            name_entry.delete(0, tk.END)
            surname_entry.delete(0, tk.END)
            id_entry.delete(0, tk.END)
            class_combobox.set('')
            subprocess.run(["python", "trainer.py"])
        else:
            messagebox.showerror("Error", "An error occurred during staff registration.")
    else:
        messagebox.showwarning("Error", "Please fill in all fields.")

# Creating the main window
root = tk.Tk()
root.iconbitmap("")
root.title("Staff Registration System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")
label_style = {"font": ("Arial", 12), "bg": "#f0f0f0"}
entry_style = {"font": ("Arial", 12)}
button_style = {
    "font": ("Arial", 12),
    "bg": "#0092A3",
    "fg": "white",
    "activebackground": "#056B76",
    "width": 15,
    "height": 2,
    "bd": 0,
    "relief": tk.FLAT
}

# User input fields and labels
tk.Label(root, text="Name:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="e")
name_entry = tk.Entry(root, **entry_style)
name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Surname:", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky="e")
surname_entry = tk.Entry(root, **entry_style)
surname_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Staff ID:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky="e")
id_entry = tk.Entry(root, **entry_style)
id_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(root, text="Department:", **label_style).grid(row=3, column=0, padx=10, pady=10, sticky="e")
class_combobox = ttk.Combobox(root, values=["Finance", "Marketing", "Sales", "Production"], state="readonly", font=("Arial", 12))
class_combobox.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Save Button
save_button = tk.Button(root, text="Save", command=save_staff, **button_style)
save_button.grid(row=4, columnspan=2, pady=20)

# Create Excel file
create_excel_file()

# Start main loop
root.mainloop()
