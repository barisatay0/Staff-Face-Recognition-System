import tkinter as tk
import subprocess
import threading
import tkinter.messagebox as messagebox

# Function that opens the staff registration screen
def open_staff_registration():
    threading.Thread(target=lambda: subprocess.run(["python", "addstaff.py"])).start()

# Function that opens the face recognition screen
def open_face_recognition():
    messagebox.showwarning("Error", "You can quit with 'q'.")
    threading.Thread(target=lambda: subprocess.run(["python", "facerec.py"])).start()

# Function that opens the staff listing function
def open_list_function():
    threading.Thread(target=lambda: subprocess.run(["python", "staffs.py"])).start()

# Creating the main window
root = tk.Tk()
root.title("Homepage")
root.geometry("300x200")
root.configure(bg="#f0f0f0")

# Styles of buttons
button_style = {
    "font": ("Arial", 12),
    "bg": "#00a8bb",
    "fg": "white",
    "activebackground": "#00646f",
    "width": 20,
    "height": 2,
    "bd": 0,
    "relief": tk.FLAT
}

# Add new staff button
new_staff_button = tk.Button(root, text="New Staff", command=open_staff_registration, **button_style)
new_staff_button.pack(pady=10)

# Face recognition button
face_recognition_button = tk.Button(root, text="Face Recognizer", command=open_face_recognition, **button_style)
face_recognition_button.pack(pady=10)

# Staff listing button
empty_button = tk.Button(root, text="Staff", command=open_list_function, **button_style)
empty_button.pack(pady=10)

# Start main loop
root.mainloop()
