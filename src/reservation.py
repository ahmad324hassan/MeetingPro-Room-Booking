from uuid import uuid4

# create a new class for reservation with a unique ID and all necessary attributes
class Reserve_a_room:
    def __init__(self, room_id, id_customer, date, debut, fin, id_reservation=None):
        self.room_id = room_id
        self.id_customer = id_customer
        self.date = date
        self.debut = debut
        self.fin = fin
        self.id_reservation = id_reservation

    def __str__(self):
        return f"Reservation ID: {self.id_reservation}, Room ID: {self.room_id}, Customer ID: {self.id_customer} Date: {self.date}, Debut {self.debut}, Time: {self.fin}"
    
    def reservation_infos(self): # This method returns the reservation details as a dictionary
        return {
            "room_id": self.room_id,
            "id_customer": self.id_customer,
            "date": self.date,
            "debut": self.debut,
            "fin": self.fin
        }