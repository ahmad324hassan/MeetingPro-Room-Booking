# Main graphical interface with Tkinter for MeetingPro
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from customers import New_Customer
from datetime import datetime
import uuid  # Import for generating unique IDs

class MeetingProApp(tk.Tk):
    def __init__(self, db_path="data.json"):  # Initialize the main application window and set up styles and tabs
        """Initialize the main application window and set up styles and tabs."""
        super().__init__()
        self.title("MeetingPro - Room Reservation Management")
        self.geometry("800x500")
        self.db = Database(db_path)  # Initialize the database
        self.tab_control = ttk.Notebook(self)  # Create the main tab control
        self.tabs = {}  # Dictionary to store tab frames
        self.create_main_tabs()  # Create all main tabs
        self.tab_control.pack(expand=1, fill="both")  # Show the tab control
        self.tab_control.select(self.tabs['Home'])  # Select the Home tab by default

        # Define a black style for all step buttons and widgets for better UI consistency
        style = ttk.Style(self)
        style.configure(
            "Black.TButton",
            foreground="black",           # Black text for all buttons
            background="#E0E0E0",         # Light gray background for contrast
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Black.TButton",
            foreground=[('active', 'black'), ('disabled', 'gray50')],
            background=[('active', '#C0C0C0'), ('disabled', '#F0F0F0')]
        )
        style.configure("TLabel", foreground="black")  # All labels in black
        style.configure("TEntry", foreground="black")  # All entry text in black
        style.configure("TCombobox", foreground="black")  # All combobox text in black
        style.configure("TRadiobutton", foreground="black")  # All radio button text in black

    def create_main_tabs(self):  # Create and initialize all main navigation tabs
        """Create and initialize all main navigation tabs."""
        tabs = [
            ("Home", self.tab_home),
            ("Add", self.tab_add),
            ("Book", self.tab_book),
            ("Display", self.tab_display)
        ]
        for name, func in tabs:
            frame = ttk.Frame(self.tab_control)  # Create a new frame for each tab
            self.tab_control.add(frame, text=name)  # Add the frame to the tab control
            self.tabs[name] = frame  # Store the frame in the tabs dictionary
            func(frame)  # Initialize the tab content

    def switch_tab(self, tab_name):  # Switch to the selected tab by name
        """Switch to the selected tab by name."""
        self.tab_control.select(self.tabs[tab_name])

    def tab_home(self, frame):  # Home tab: navigation buttons to other main tabs
        """Home tab: navigation buttons to other main tabs."""
        btn_add = ttk.Button(frame, text="Add", command=lambda: self.switch_tab("Add"), style="Black.TButton")
        btn_book = ttk.Button(frame, text="Book", command=lambda: self.switch_tab("Book"), style="Black.TButton")
        btn_display = ttk.Button(frame, text="Display", command=lambda: self.switch_tab("Display"), style="Black.TButton")
        btn_add.pack(pady=30)
        btn_book.pack(pady=30)
        btn_display.pack(pady=30)

    def tab_add(self, frame):  # Tab for adding a new customer or a new room
        """Tab for adding a new customer or a new room."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear the frame before adding widgets
        # Buttons to choose between adding a customer or a room
        btn_customer = ttk.Button(frame, text="Add new customer", command=lambda: self.show_customer_form(frame), style="Black.TButton")
        btn_room = ttk.Button(frame, text="Add new room", command=lambda: self.show_room_form(frame), style="Black.TButton")
        btn_customer.pack(pady=20)
        btn_room.pack(pady=20)

    def show_customer_form(self, frame):  # Display the form to add a new customer
        """Display the form to add a new customer."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous widgets
        # Input fields for customer information
        ttk.Label(frame, text="Last Name:").grid(row=0, column=0, sticky="e")
        last_name_entry = ttk.Entry(frame)
        last_name_entry.grid(row=0, column=1)
        ttk.Label(frame, text="First Name:").grid(row=1, column=0, sticky="e")
        first_name_entry = ttk.Entry(frame)
        first_name_entry.grid(row=1, column=1)
        ttk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e")
        email_entry = ttk.Entry(frame)
        email_entry.grid(row=2, column=1)

        def validate():  # Validate and add a new customer to the database
            """Validate and add a new customer to the database."""
            last_name = last_name_entry.get()
            first_name = first_name_entry.get()
            email = email_entry.get()
            if not (last_name and first_name and email):
                messagebox.showerror("Error", "Please fill in all fields.")  # Error if any field is empty
                return
            # Check for unique email
            if any(c.email == email for c in self.db.get_customers()):
                messagebox.showerror("Error", "A customer with this email already exists.")  # Error if email exists
                return
            new_customer = New_Customer(last_name, first_name, email)
            self.db.add_customer(new_customer)  # Add customer to database
            messagebox.showinfo("Success", "Customer added!")  # Success message
            self.start_booking_for_customer(new_customer)  # Go to booking tab with this customer preselected

        def cancel():  # Cancel and return to add tab
            """Cancel and return to add tab."""
            self.tab_add(frame)

        ttk.Button(frame, text="Validate", command=validate, style="Black.TButton").grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=cancel).grid(row=3, column=1, pady=10)

    def start_booking_for_customer(self, customer):  # Open the booking tab and pre-select the given customer
        """Open the booking tab and pre-select the given customer."""
        self.tab_control.select(self.tabs['Book'])
        frame = self.tabs['Book']
        self.tab_book(frame, preselected_customer=customer)

    def show_room_form(self, frame):  # Display the form to add a new room
        """Display the form to add a new room."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous widgets
        # Input fields for room information
        ttk.Label(frame, text="Room ID:").grid(row=0, column=0, sticky="e")
        id_entry = ttk.Entry(frame)
        id_entry.grid(row=0, column=1)
        ttk.Label(frame, text="Room type:").grid(row=1, column=0, sticky="e")
        type_cb = ttk.Combobox(frame, values=["standard", "conference", "informatics"], state="readonly")
        type_cb.grid(row=1, column=1)
        ttk.Label(frame, text="Capacity:").grid(row=2, column=0, sticky="e")
        capacity_cb = ttk.Combobox(frame, state="readonly")
        capacity_cb.grid(row=2, column=1)

        def update_capacity(*args):  # Update capacity options based on room type selection
            """Update capacity options based on room type selection."""
            t = type_cb.get()
            if t == "standard" or t == "informatics":
                capacity_cb['values'] = [1, 2, 3, 4]
            elif t == "conference":
                capacity_cb['values'] = list(range(4, 11))
            else:
                capacity_cb['values'] = []
            capacity_cb.set("")
        type_cb.bind("<<ComboboxSelected>>", update_capacity)

        def validate():  # Validate and add a new room to the database
            """Validate and add a new room to the database."""
            room_id = id_entry.get()
            room_type = type_cb.get()
            capacity = capacity_cb.get()
            if not (room_id and room_type and capacity):
                messagebox.showerror("Error", "Please fill in all fields.")  # Error if any field is empty ☻
                return
            # Check for unique room ID
            if any(str(s.id) == str(room_id) for s in self.db.get_rooms()):
                messagebox.showerror("Error", "This room ID already exists.")  # Error if room ID exists :(
                return
            from room import type_of_room, New_Room
            # Create the room type object
            room_type_obj = type_of_room(
                Standard="Yes" if room_type == "standard" else "No",
                Conference="Yes" if room_type == "conference" else "No",
                Informatics="Yes" if room_type == "informatics" else "No"
            )
            try:
                capacity_int = int(capacity)
            except Exception:
                messagebox.showerror("Error", "Capacity must be a number.")  # Error if capacity is not a number
                return
            new_room = New_Room(room_id, capacity_int, room_type_obj)  # Create the room object
            self.db.add_room(new_room)  # Add the new room to the database
            messagebox.showinfo("Success", "Room added!")  # Success message
            self.tab_add(frame)

        def cancel():  # Cancel and return to add tab
            """Cancel and return to add tab."""
            self.tab_add(frame)

        ttk.Button(frame, text="Validate", command=validate, style="Black.TButton").grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=cancel).grid(row=3, column=1, pady=10)

    def tab_book(self, frame, preselected_customer=None):  # Booking tab: step 1 - select customer, date, and time
        """Booking tab: step 1 - select customer, date, and time."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous widgets

        # Error label at the top for displaying errors to the user
        error_var = tk.StringVar()
        error_label = ttk.Label(frame, textvariable=error_var, foreground="red")
        error_label.grid(row=0, column=2, padx=10, sticky="w")

        # Customer selection
        ttk.Label(frame, text="Customer:").grid(row=1, column=0, sticky="e")
        customers_list = self.db.get_customers()
        customer_values = [f"{c.name} {c.surname}" for c in customers_list]
        customer_ids = [c.id_customer for c in customers_list]
        customer_cb = ttk.Combobox(frame, values=customer_values, state="readonly")
        customer_cb.grid(row=1, column=1)
        if preselected_customer:
            try:
                idx = customer_ids.index(preselected_customer.id_customer)
                customer_cb.current(idx)
            except ValueError:
                pass

        # Date and time selection
        ttk.Label(frame, text="Date (DD/MM/YYYY):").grid(row=2, column=0, sticky="e")
        date_entry = ttk.Entry(frame)
        date_entry.grid(row=2, column=1)
        ttk.Label(frame, text="Start time (HH:MM):").grid(row=3, column=0, sticky="e")
        start_time = ttk.Entry(frame, width=7)
        start_time.grid(row=3, column=1)
        ttk.Label(frame, text="End time (HH:MM):").grid(row=4, column=0, sticky="e")
        end_time = ttk.Entry(frame, width=7)
        end_time.grid(row=4, column=1)

        # Room type selection
        ttk.Label(frame, text="Room type:").grid(row=5, column=0, sticky="e")
        type_var = tk.StringVar()
        type_frame = ttk.Frame(frame)
        type_frame.grid(row=5, column=1, sticky="w")
        types = ["standard", "conference", "informatics"]
        for t in types:
            ttk.Radiobutton(type_frame, text=t.capitalize(), variable=type_var, value=t).pack(side="left", padx=10)

        # Capacity selection
        ttk.Label(frame, text="Capacity needed:").grid(row=6, column=0, sticky="e")
        capacity_var = tk.StringVar()
        capacity_cb = ttk.Combobox(frame, textvariable=capacity_var, state="readonly")
        capacity_cb.grid(row=6, column=1)

        def update_capacity_options(*args):  # Dynamically update capacity options based on selected room type
            """Dynamically update capacity options based on selected room type."""
            t = type_var.get()
            if t == "standard" or t == "informatics":
                capacity_cb['values'] = [1, 2, 3, 4]
            elif t == "conference":
                capacity_cb['values'] = list(range(4, 11))
            else:
                capacity_cb['values'] = []
            capacity_cb.set("")
        type_var.trace_add("write", lambda *args: update_capacity_options())

        def search_rooms():  # Search and display available rooms based on user input
            """Search and display available rooms based on user input."""
            error_var.set("")  # Clear previous errors
            customer_index = customer_cb.current()
            if customer_index == -1:
                error_var.set("Please select a customer.")  # Error if no customer selected
                return
            customer_id = customer_ids[customer_index]
            customer_name = customer_values[customer_index]
            date_str = date_entry.get()
            h_start = start_time.get()
            h_end = end_time.get()
            room_type = type_var.get()
            try:
                needed_capacity = int(capacity_var.get())
            except Exception:
                needed_capacity = None
            if not (date_str and h_start and h_end and room_type and needed_capacity):
                error_var.set("Please fill in all fields.")  # Error if any field is empty
                return
            from datetime import datetime
            try:
                start_dt = datetime.strptime(f"{date_str} {h_start}", "%d/%m/%Y %H:%M")
                end_dt = datetime.strptime(f"{date_str} {h_end}", "%d/%m/%Y %H:%M")
                if end_dt <= start_dt:
                    raise Exception
            except Exception:
                error_var.set("Invalid date or time format, or end time before start time.")  # Error if date/time is invalid
                return

            # Filter rooms by type and capacity
            all_rooms = self.db.get_rooms()
            filtered_rooms = []
            for s in all_rooms:
                if ((getattr(s.room, "Standard", "No") == "Yes" and room_type == "standard") or
                    (getattr(s.room, "Conference", "No") == "Yes" and room_type == "conference") or
                    (getattr(s.room, "Informatics", "No") == "Yes" and room_type == "informatics")):
                    if s.capacity >= needed_capacity:
                        filtered_rooms.append(s)

            # Remove rooms that are already reserved at the selected time
            available_rooms = []
            for room in filtered_rooms:
                available = True
                for r in self.db.get_reservations():
                    if r.room_id == room.id and r.date == date_str:
                        # Build a complete datetime if needed for comparison
                        try:
                            r_start = datetime.fromisoformat(r.debut)
                            r_end = datetime.fromisoformat(r.fin)
                        except ValueError:
                            r_start = datetime.strptime(f"{r.date} {r.debut}", "%d/%m/%Y %H:%M")
                            r_end = datetime.strptime(f"{r.date} {r.fin}", "%d/%m/%Y %H:%M")
                        if not (end_dt <= r_start or start_dt >= r_end):
                            available = False
                            break
                if available:
                    available_rooms.append(room)

            # Display available rooms in a combobox
            for widget in frame.winfo_children():
                if getattr(widget, "is_dynamic", False):
                    widget.destroy()
            ttk.Label(frame, text="Available room:").grid(row=7, column=0, sticky="e")
            room_cb = ttk.Combobox(frame, state="readonly")
            room_cb['values'] = [f"{s.id} (capacity: {s.capacity})" for s in available_rooms]
            room_cb.grid(row=7, column=1)
            room_cb.is_dynamic = True

            def confirm_booking():  # Confirm the booking and add the reservation
                """Confirm the booking and add the reservation."""
                room_index = room_cb.current()
                if room_index == -1:
                    messagebox.showerror("Error", "Please select an available room.")  # Error if no room selected
                    return
                selected_room = available_rooms[room_index]
                from reservation import Reserve_a_room
                reservation_id = str(uuid.uuid4())  # Generate a unique id for the reservation
                reservation = Reserve_a_room(selected_room.id, customer_id, date_str, h_start, h_end, id_reservation=reservation_id)
                self.db.add_reservation(reservation)  # Add reservation to database
                messagebox.showinfo("Success", f"Room {selected_room.id} booked for {customer_name}!")  # Success message
                self.tab_control.select(self.tabs['Home'])  # Return to home tab

            btn_confirm = ttk.Button(frame, text="Confirm booking", command=confirm_booking, style="Black.TButton")
            btn_confirm.grid(row=8, column=0, columnspan=2, pady=10)
            btn_confirm.is_dynamic = True

        ttk.Button(frame, text="Search available rooms", command=search_rooms, style="Black.TButton").grid(row=9, column=0, columnspan=2, pady=15)

    def tab_display(self, frame):  # Display tab: show customers, rooms, reservations, and availability
        """Display tab: show customers, rooms, reservations, and availability."""
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous widgets
        tree = ttk.Treeview(frame) # Create a treeview to display datas 
        tree.pack(expand=True, fill="both", pady=10)

        # Increase row height for better readability
        style = ttk.Style()
        style.configure("Treeview", rowheight=40)

        def show_customers():  # Display all customers in the treeview
            """Display all customers in the treeview."""
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "name", "surname", "email")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=150)
            for i, customer in enumerate(self.db.get_customers(), 1):
                tree.insert('', 'end', text=str(i), values=(customer.id_customer, customer.name, customer.surname, customer.email))

        def show_rooms():  # Display all rooms in the treeview
            """Display all rooms in the treeview."""
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "capacity", "type")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=120)
            for i, room_obj in enumerate(self.db.get_rooms(), 1):
                room_type = "Standard" if room_obj.room.Standard == "Yes" else "Conference" if room_obj.room.Conference == "Yes" else "Informatics"
                tree.insert('', 'end', text=str(i), values=(room_obj.id, room_obj.capacity, room_type))

        def show_reservations():  # Display all reservations with customer name, room, date, and times
            """Display all reservations with customer name, room, date, and times."""
            tree.delete(*tree.get_children())
            tree['columns'] = ("room_id", "customer", "date", "start", "end")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.replace('_', ' ').capitalize())
                tree.column(col, width=140)
            for i, r in enumerate(self.db.get_reservations(), 1):
                client = next((c for c in self.db.get_customers() if c.id_customer == r.id_customer), None)
                client_name = f"{client.name} {client.surname}" if client else r.id_customer
                tree.insert('', 'end', text=str(i), values=(r.room_id, client_name, r.date, r.debut, r.fin))

        def show_availability():  # Display for each room all available hourly slots (from 8am to 8pm)
            """Display for each room all available hourly slots (from 8am to 8pm)."""
            from datetime import datetime, timedelta
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "capacity", "type", "available_slots")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            tree.column("id", width=60)
            tree.column("capacity", width=80)
            tree.column("type", width=100)
            tree.column("available_slots", width=400)  # Increase width for all slots

            now = datetime.now()
            date_str = now.strftime("%d/%m/%Y")
            for i, room_obj in enumerate(self.db.get_rooms(), 1):
                slots = []
                for h in range(8, 20):  # Slots from 8am to 8pm
                    slot_start = now.replace(hour=h, minute=0, second=0, microsecond=0)
                    slot_end = slot_start + timedelta(hours=1)
                    overlap = False
                    for r in self.db.get_reservations():
                        if r.room_id == room_obj.id and r.date == date_str:
                            try:
                                r_start = datetime.fromisoformat(r.debut)
                                r_end = datetime.fromisoformat(r.fin)
                            except ValueError:
                                r_start = datetime.strptime(f"{r.date} {r.debut}", "%d/%m/%Y %H:%M")
                                r_end = datetime.strptime(f"{r.date} {r.fin}", "%d/%m/%Y %H:%M")
                            if not (slot_end <= r_start or slot_start >= r_end):
                                overlap = True
                                break
                    if not overlap:
                        slots.append(f"{h:02d}:00-{h+1:02d}:00")
                room_type = "Standard" if room_obj.room.Standard == "Yes" else "Conference" if room_obj.room.Conference == "Yes" else "Informatics"
                # Split the list into two lines for better readability
                if slots:
                    mid = (len(slots) + 1) // 2
                    slots_str = ", ".join(slots[:mid]) + "\n" + ", ".join(slots[mid:])
                else:
                    slots_str = "Aucun"
                tree.insert('', 'end', text=str(i), values=(room_obj.id, room_obj.capacity, room_type, slots_str))

        # Buttons to display each category, all in blue style
        btn_customers = ttk.Button(frame, text="Show Customers", command=show_customers, style="Black.TButton")
        btn_rooms = ttk.Button(frame, text="Show Rooms", command=show_rooms, style="Black.TButton")
        btn_reservations = ttk.Button(frame, text="Show Reservations", command=show_reservations, style="Black.TButton")
        btn_availability = ttk.Button(frame, text="Show Availability", command=show_availability, style="Black.TButton")
        btn_customers.pack(pady=5)
        btn_rooms.pack(pady=5)
        btn_reservations.pack(pady=5)
        btn_availability.pack(pady=5)
        show_customers()  # Show customers by default

if __name__ == "__main__":
    app = MeetingProApp()
    app.mainloop()
