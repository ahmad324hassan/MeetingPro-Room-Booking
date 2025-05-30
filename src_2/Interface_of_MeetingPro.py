import tkinter as tk

def create_interface():
    # Create the main window
    root = tk.Tk()
    root.title("Interface Creation Example")
    
    # Set the size of the window
    root.geometry("800x600")
    
    # Create a label
    label = tk.Label(root, text="Welcome to the Interface!")
    label.pack(pady=50)
    label.config(font=("Arial", 24))  # Set the font size and type
    label.size = (300, 20)  # Set the size of the label
    


    # Create a button to add a new customer
    button_new_customer = tk.Button(root, text="Add a new customer", command=lambda: print("Button clicked!"), bg="blue", fg="white")
    button_new_customer.pack(pady=30)

    # Create a button to add a new reservation
    button_reservation = tk.Button(root, text="Add a new reservation", command=lambda: print("Reservation button clicked!"), bg="blue", fg="white")
    button_reservation.pack(pady=30)

    # Create a button to add to display informations
    button_display = tk.Button(root, text="Display Information",command=lambda: print("Display Information button clicked!"), bg="blue", fg="white")
    button_display.pack(pady=30)


    
    # Start the GUI event loop
    root.mainloop()

create_interface() 
