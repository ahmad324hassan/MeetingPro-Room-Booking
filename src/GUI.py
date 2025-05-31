# Main graphical interface with Tkinter for MeetingPro
import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from customers import New_Customer

class MeetingProApp(tk.Tk):
    def __init__(self, db_path="data.json"):
        super().__init__()
        self.title("MeetingPro - Room Reservation Management")
        self.geometry("800x500")
        self.db = Database(db_path)  # Initialize the database
        self.tab_control = ttk.Notebook(self)  # Create the main tab control
        self.tabs = {}  # Dictionary to store tab frames
        self.create_main_tabs()  # Create all main tabs
        self.tab_control.pack(expand=1, fill="both")  # Show the tab control
        self.tab_control.select(self.tabs['Home'])  # Select the Home tab by default

    def create_main_tabs(self):
        # Main tabs for navigation
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

    def switch_tab(self, tab_name):
        # Switch to the selected tab
        self.tab_control.select(self.tabs[tab_name])

    def tab_home(self, frame):
        # Home tab with navigation buttons
        btn_add = ttk.Button(frame, text="Add", command=lambda: self.switch_tab("Add"))
        btn_book = ttk.Button(frame, text="Book", command=lambda: self.switch_tab("Book"))
        btn_display = ttk.Button(frame, text="Display", command=lambda: self.switch_tab("Display"))
        btn_add.pack(pady=30)
        btn_book.pack(pady=30)
        btn_display.pack(pady=30)

    def tab_add(self, frame):
        # Clear the frame before adding widgets
        for widget in frame.winfo_children():
            widget.destroy()
        # Buttons to choose between adding a customer or a room
        btn_customer = ttk.Button(frame, text="Add new customer", command=lambda: self.show_customer_form(frame))
        btn_room = ttk.Button(frame, text="Add new room", command=lambda: self.show_room_form(frame))
        btn_customer.pack(pady=20)
        btn_room.pack(pady=20)

    def show_customer_form(self, frame):
        # Form to add a new customer
        for widget in frame.winfo_children():
            widget.destroy()
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

        def validate():
            # Get input values
            last_name = last_name_entry.get()
            first_name = first_name_entry.get()
            email = email_entry.get()
            if not (last_name and first_name and email):
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            # Check for unique email
            if any(c.email == email for c in self.db.get_customers()):
                messagebox.showerror("Error", "A customer with this email already exists.")
                return
            new_customer = New_Customer(last_name, first_name, email)
            self.db.add_customer(new_customer)
            messagebox.showinfo("Success", "Customer added!")
            for widget in frame.winfo_children():
                widget.destroy()
            ttk.Label(frame, text="Customer added!").pack(pady=10)
            ttk.Button(frame, text="Book a room for this customer", command=lambda: self.start_booking_for_customer(new_customer)).pack(pady=10)
            ttk.Button(frame, text="Add another customer", command=lambda: self.show_customer_form(frame)).pack(pady=10)
            ttk.Button(frame, text="Back to Add menu", command=lambda: self.tab_add(frame)).pack(pady=10)

        def cancel():
            self.tab_add(frame)

        ttk.Button(frame, text="Validate", command=validate).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=cancel).grid(row=3, column=1, pady=10)

    def start_booking_for_customer(self, customer):
        # Open the booking tab and pre-select the given customer
        self.tab_control.select(self.tabs['Book'])
        frame = self.tabs['Book']
        self.tab_book(frame, preselected_customer=customer)

    def show_room_form(self, frame):
        # Form to add a new room
        for widget in frame.winfo_children():
            widget.destroy()
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
        def update_capacity(*args):
            # Update capacity options based on room type
            t = type_cb.get()
            if t == "standard" or t == "informatics":
                capacity_cb['values'] = [1,2,3,4]
            elif t == "conference":
                capacity_cb['values'] = list(range(4,11))
            else:
                capacity_cb['values'] = []
            capacity_cb.set("")
        type_cb.bind("<<ComboboxSelected>>", update_capacity)
        def validate():
            # Get input values
            room_id = id_entry.get()
            room_type = type_cb.get()
            capacity = capacity_cb.get()
            if not (room_id and room_type and capacity):
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            # Check for unique room ID
            if any(s.id == room_id for s in self.db.get_rooms()):
                messagebox.showerror("Error", "This room ID already exists.")
                return
            from room import type_of_room, New_Room
            # Create the room type object
            room_type_obj = type_of_room(
                Standard="Yes" if room_type == "standard" else "No",
                Conference="Yes" if room_type == "conference" else "No",
                Informatics="Yes" if room_type == "informatics" else "No"
            )
            self.db.add_room(New_Room(room_id, int(capacity), room_type_obj))  # Add the new room to the database
            messagebox.showinfo("Success", "Room added!")
            self.tab_add(frame)
        def cancel():
            self.tab_add(frame)
        ttk.Button(frame, text="Validate", command=validate).grid(row=3, column=0, pady=10)
        ttk.Button(frame, text="Cancel", command=cancel).grid(row=3, column=1, pady=10)

    def tab_book(self, frame, preselected_customer=None):
        # Booking tab: step 1 - select customer, date, and time
        for widget in frame.winfo_children():
            widget.destroy()
        # Customer selection
        ttk.Label(frame, text="Customer:").grid(row=0, column=0, sticky="e")
        customers_list = self.db.get_customers()
        customer_values = [f"{c.name} {c.surname}" for c in customers_list]
        customer_ids = [c.id_customer for c in customers_list]
        customer_cb = ttk.Combobox(frame, values=customer_values, state="readonly")
        customer_cb.grid(row=0, column=1)
        if preselected_customer:
            try:
                idx = customer_ids.index(preselected_customer.id_customer)
                customer_cb.current(idx)
            except ValueError:
                pass

        # Date and time selection
        ttk.Label(frame, text="Date (DD/MM/YYYY):").grid(row=1, column=0, sticky="e")
        date_entry = ttk.Entry(frame)
        date_entry.grid(row=1, column=1)
        ttk.Label(frame, text="Start time (HH:MM):").grid(row=2, column=0, sticky="e")
        start_time = ttk.Entry(frame, width=7)
        start_time.grid(row=2, column=1)
        ttk.Label(frame, text="End time (HH:MM):").grid(row=3, column=0, sticky="e")
        end_time = ttk.Entry(frame, width=7)
        end_time.grid(row=3, column=1)

        # Room type selection
        ttk.Label(frame, text="Room type:").grid(row=4, column=0, sticky="e")
        type_var = tk.StringVar()
        type_frame = ttk.Frame(frame)
        type_frame.grid(row=4, column=1, sticky="w")
        types = ["standard", "conference", "informatics"]
        for t in types:
            ttk.Radiobutton(type_frame, text=t.capitalize(), variable=type_var, value=t).pack(side="left", padx=10)

        # Capacity selection
        ttk.Label(frame, text="Capacity needed:").grid(row=5, column=0, sticky="e")
        capacity_var = tk.StringVar()
        capacity_cb = ttk.Combobox(frame, textvariable=capacity_var, state="readonly")
        capacity_cb.grid(row=5, column=1)

        # Update capacity options when room type changes
        def update_capacity_options(*args):
            t = type_var.get()
            if t == "standard" or t == "informatics":
                capacity_cb['values'] = [1, 2, 3, 4]
            elif t == "conference":
                capacity_cb['values'] = list(range(4, 11))
            else:
                capacity_cb['values'] = []
            capacity_cb.set("")
        type_var.trace_add("write", lambda *args: update_capacity_options())

        # Button to search for available rooms
        def search_rooms():
            customer_index = customer_cb.current()
            if customer_index == -1:
                messagebox.showerror("Error", "Please select a customer.")
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
                messagebox.showerror("Error", "Please fill in all fields.")
                return
            from datetime import datetime
            try:
                start_dt = datetime.strptime(f"{date_str} {h_start}", "%d/%m/%Y %H:%M")
                end_dt = datetime.strptime(f"{date_str} {h_end}", "%d/%m/%Y %H:%M")
                if end_dt <= start_dt:
                    raise Exception
            except Exception:
                messagebox.showerror("Error", "Invalid date or time format, or end time before start time.")
                return

            # Filter rooms by type and capacity
            all_rooms = self.db.get_rooms()
            filtered_rooms = []
            for s in all_rooms:
                if ((s.room.Standard == "Yes" and room_type == "standard") or
                    (s.room.Conference == "Yes" and room_type == "conference") or
                    (s.room.Informatics == "Yes" and room_type == "informatics")):
                    if s.capacity >= needed_capacity:
                        filtered_rooms.append(s)

            # Filter available rooms (no overlap)
            available_rooms = []
            for room in filtered_rooms:
                available = True
                for r in self.db.get_reservations():
                    from datetime import datetime
                    r_start = datetime.fromisoformat(r.debut)
                    r_end = datetime.fromisoformat(r.fin)
                    if r.room_id == room.id and not (end_dt <= r_start or start_dt >= r_end):
                        available = False
                        break
                if available:
                    available_rooms.append(room)

            # Show available rooms in a combobox
            for widget in frame.winfo_children():
                if getattr(widget, "is_dynamic", False):
                    widget.destroy()
            ttk.Label(frame, text="Available room:").grid(row=6, column=0, sticky="e")
            room_cb = ttk.Combobox(frame, state="readonly")
            room_cb['values'] = [f"{s.id} (capacity: {s.capacity})" for s in available_rooms]
            room_cb.grid(row=6, column=1)
            room_cb.is_dynamic = True  # Mark as dynamic to clean up later

            def confirm_booking():
                room_index = room_cb.current()
                if room_index == -1:
                    messagebox.showerror("Error", "Please select an available room.")
                    return
                selected_room = available_rooms[room_index]
                from reservation import Reserve_a_room
                self.db.add_reservation(Reserve_a_room(selected_room.id, customer_id, date_str, h_start, h_end))
                messagebox.showinfo("Success", f"Room {selected_room.id} booked for {customer_name}!")
                self.tab_book(frame)

            btn_confirm = ttk.Button(frame, text="Confirm booking", command=confirm_booking)
            btn_confirm.grid(row=7, column=0, columnspan=2, pady=10)
            btn_confirm.is_dynamic = True

        ttk.Button(frame, text="Search available rooms", command=search_rooms).grid(row=8, column=0, columnspan=2, pady=15)

    def tab_display(self, frame):
        # Display tab: show customers, rooms, reservations, and availability
        for widget in frame.winfo_children():
            widget.destroy()
        tree = ttk.Treeview(frame)
        tree.pack(expand=True, fill="both", pady=10)
        def show_customers():
            # Display all customers in the treeview
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "name", "surname", "email")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=150)
            for i, customer in enumerate(self.db.get_customers(), 1):
                tree.insert('', 'end', text=str(i), values=(customer.id_customer, customer.name, customer.surname, customer.email))
        def show_rooms():
            # Display all rooms in the treeview
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "capacity", "type")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=120)
            for i, room_obj in enumerate(self.db.get_rooms(), 1):
                # Determine room type for display
                room_type = "Standard" if room_obj.room.Standard == "Yes" else "Conference" if room_obj.room.Conference == "Yes" else "Informatics"
                tree.insert('', 'end', text=str(i), values=(room_obj.id, room_obj.capacity, room_type))
        def show_reservations():
            # Display all reservations in the treeview
            tree.delete(*tree.get_children())
            tree['columns'] = ("room_id", "customer_id", "date", "start", "end")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.replace('_', ' ').capitalize())
                tree.column(col, width=140)
            for i, r in enumerate(self.db.get_reservations(), 1):
                tree.insert('', 'end', text=str(i), values=(r.room_id, r.id_customer, r.date, r.debut, r.fin))
        def show_availability():
            # Display room availability for today
            from datetime import datetime
            tree.delete(*tree.get_children())
            tree['columns'] = ("id", "capacity", "type", "availability")
            tree.heading("#0", text="#")
            tree.column("#0", width=30)
            for col in tree['columns']:
                tree.heading(col, text=col.capitalize())
                tree.column(col, width=120)
            now = datetime.now()
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            for i, room_obj in enumerate(self.db.get_rooms(), 1):
                available = True
                for r in self.db.get_reservations():
                    if r.room_id == room_obj.id:
                        r_start = datetime.fromisoformat(r.debut)
                        r_end = datetime.fromisoformat(r.fin)
                        # If reservation overlaps with now, mark as unavailable
                        if not (end_of_day <= r_start or now >= r_end):
                            available = False
                            break
                status = "Available" if available else "Unavailable"
                room_type = "Standard" if room_obj.room.Standard == "Yes" else "Conference" if room_obj.room.Conference == "Yes" else "Informatics"
                tree.insert('', 'end', text=str(i), values=(room_obj.id, room_obj.capacity, room_type, status))
        # Buttons to display each category
        btn_customers = ttk.Button(frame, text="Show Customers", command=show_customers)
        btn_rooms = ttk.Button(frame, text="Show Rooms", command=show_rooms)
        btn_reservations = ttk.Button(frame, text="Show Reservations", command=show_reservations)
        btn_availability = ttk.Button(frame, text="Show Availability", command=show_availability)
        btn_customers.pack(pady=5)
        btn_rooms.pack(pady=5)
        btn_reservations.pack(pady=5)
        btn_availability.pack(pady=5)
        # Show customers by default
        show_customers()

if __name__ == "__main__":
    app = MeetingProApp()
    app.mainloop()
