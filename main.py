# Example usage of the Database module (updated for new class and method names)
from src.customers import New_Customer
from src.room import New_Room, type_of_room
from src.reservation import Reserve_a_room
from src.database import Database
from datetime import datetime, timedelta

if __name__ == "__main__":
    db = Database("data.json")

    # Add a customer
    customer = New_Customer(name="Alice", surname="Dupont", email="alice@example.com")
    db.add_customer(customer)

    # Add a room
    room_type = type_of_room(Standard="Yes", Conference="No", Informatics="No")
    room = New_Room(id="R1", capacity=4, room=room_type)
    db.add_room(room)

    # Create a reservation
    date_str = datetime.now().strftime("%d/%m/%Y")
    start_time = datetime.now().strftime("%H:%M")
    end_time = (datetime.now() + timedelta(hours=2)).strftime("%H:%M")
    reservation = Reserve_a_room(room_id=room.id, id_customer=customer.id_customer, date=date_str, debut=start_time, fin=end_time)
    db.add_reservation(reservation)

    # Display customers, rooms, and reservations
    print("Customers:", db.get_customers())
    print("Rooms:", db.get_rooms())
    print("Reservations:", db.get_reservations())



