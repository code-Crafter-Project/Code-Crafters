def open_gui():
   import tkinter as tk
   from tkinter import simpledialog, messagebox
   import random


   root = tk.Tk()
   root.geometry('500x500')
   root.title('Integrated Library System')

   root.configure(bg="BLUE")
   # Function to change the color of a specific label
   def change_label_color(label):
   # Generate a random color
    color = "Light green".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Update the label's foreground (text) color
    label.config(fg=color)


   Label = tk.Label(root, text='WELCOME TO VANDERBIJLPARK PUBLIC LIBRARY', font=('Bold', 25))
   Label.pack(padx=10, pady=20)

   Label.configure(bg=root.cget("bg"))
   change_label_color(Label)

   
   
   
   def checkout_book():
      messagebox.showinfo("Checkout", f"Book checked out successfully!")
     
     
   def checkin_book():
      messagebox.showinfo("Check-in", f"Book checked in successfully!")

   def get_input():
    result = simpledialog.askstring("Input", "Enter your message:")
    if result:
        messagebox.showinfo("Thank You", f"Enquiry received ")
   # Create two buttons
   button1 = tk.Button(root, text="Check-Out",command=checkin_book , width=30, height=5, bg="light green", fg="black")
   button2 = tk.Button(root, text="Check-In", command=checkout_book , width=30, height=5, bg="light green", fg="black")
   button3 = tk.Button(root, text="Send Enquiries", command=get_input, width=30, height=5, bg="light green", fg="black")

   # Use the pack() manager to place them side by side
   button1.pack(side=tk.LEFT, padx=100)
   button2.pack(side=tk.LEFT, padx=100)
   button3.pack(side=tk.LEFT, padx=100)

   root.mainloop()