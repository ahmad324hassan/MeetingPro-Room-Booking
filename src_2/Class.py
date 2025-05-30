from uuid import uuid4

#Add a new customer

class New_Customer:
    def __init__(self, name: str, surname: str, email: str, id_customer: str):
        self.id_customer = str(uuid4())
        self.name = name
        self.surname = surname
        self.email = email
    def __str__(self):
        return f"Client: {self.name} {self.surname}, Email: {self.email}, ID: {self.id_customer}"
    
#Add a new room
class type_of_room:
    def __init__(self, Standard: str, Conférence: str, Informatique: str):
        self.Standard = Standard
        self.Conférence = Conférence
        self.Informatique = Informatique    
    def __str__(self):  
        return f"Room Types: Standard: {self.Standard}, Conference: {self.Conférence}, IT: {self.Informatique}"

#Add a new room with capacity
class New_Room:
    def __init__(self, id: int, capacity: int, room: type_of_room):
        self.id = id
        self.capacity = capacity
        self.room = room
    def __str__(self):
        return f"Room ID: {self.id}, Capacity: {self.capacity}, Type: {self.room}"
    
    
#Reserve a room

class Reserve_a_room:
    def __init__(self, room_id: str, id_customer: str, date: int, debut: int, fin: int):
        self.id_customer = str(uuid4())
        self.room_id = room_id
        self.date = date
        self.debut = debut
        self.fin = fin

    def __str__(self):
        return f"Reservation ID: {self.room_id}, Customer ID: {self.id_customer} Date: {self.date}, Debut {self.debut}, Time: {self.fin}"
    




