import tkinter as tk
import json
import subprocess

def register():
    username = username_entry.get()
    password = password_entry.get()
    
    # Check if the user already exists
    if username in users:
        message_label.config(text="User already exists!")
    else:
        users[username] = {"password": password, "history": []}
        save_users()
        message_label.config(text="Registration successful!")

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Check if the user exists and password matches
    if username in users and users[username]["password"] == password:
        message_label.config(text="Login successful!")
        # Perform actions after login
        
        # Add example history entry
        users[username]["history"].append("Logged in at: example_time")
        save_users()
        
        # Launch the Jupyter Notebook
        subprocess.run(["jupyter", "notebook", "AI Rec System.ipynb"], shell=True)
    else:
        message_label.config(text="Invalid username or password!")

def save_users():
    with open('users.json', 'w') as file:
        json.dump(users, file)

# Load existing users or create an empty dictionary
try:
    with open('users.json', 'r') as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

# Create the Tkinter window
window = tk.Tk()
window.title("Registration and Login")
window.geometry("300x200")

# Create the labels, entries, and buttons
username_label = tk.Label(window, text="Username:")
username_label.pack()

username_entry = tk.Entry(window)
username_entry.pack()

password_label = tk.Label(window, text="Password:")
password_label.pack()

password_entry = tk.Entry(window, show="*")
password_entry.pack()

register_button = tk.Button(window, text="Register", command=register)
register_button.pack()

login_button = tk.Button(window, text="Login", command=login)
login_button.pack()

message_label = tk.Label(window, text="")
message_label.pack()

# Run the Tkinter event loop
window.mainloop()