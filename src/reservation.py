from uuid import uuid4

class Reserve_a_room:
    def __init__(self, room_id: str, id_customer: str, date: int, debut: int, fin: int):
        self.room_id = room_id
        self.id_customer = id_customer
        self.date = date
        self.debut = debut
        self.fin = fin

    def __str__(self):
        return f"Reservation ID: {self.room_id}, Customer ID: {self.id_customer} Date: {self.date}, Debut {self.debut}, Time: {self.fin}"
    
    def reservation_infos(self):
        return {
            "room_id": self.room_id,
            "id_customer": self.id_customer,
            "date": self.date,
            "debut": self.debut,
            "fin": self.fin
        }