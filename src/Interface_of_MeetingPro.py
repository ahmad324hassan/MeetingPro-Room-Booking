import tkinter as tk

def create_interface():
    # Create the main window
    root = tk.Tk()
    root.title("Interface Creation Example")
    
    # Set the size of the window
    root.geometry("800x600")
    
    # Create a label
    label = tk.Label(root, text="Welcome to the Interface!")
    label.pack(pady=90)
    
    # Create a button
    button = tk.Button(root, text="Add a new customer", command=lambda: print("Button clicked!"))
    button.pack(pady=10)
    
    # Start the GUI event loop
    root.mainloop()

create_interface()
