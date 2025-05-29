#Ajout d'un nouveau client

class New_Customer:
    def __init__(self, name: str, surname: str, email: str):
        self.name = name
        self.surname = surname
        self.email = email
    def __str__(self):
        return f"Client: {self.name} {self.surname}, Email: {self.email}"
    
#Ajout d'une nouvelle salle

class type_of_room:
    def __init__(self, Standard: str, Conférence: str, Informatique: str):
        self.Standard = Standard
        self.Conférence = Conférence
        self.Informatique = Informatique    
    def __str__(self):  
        return f"Room Types: Standard: {self.Standard}, Conference: {self.Conférence}, IT: {self.Informatique}"


class New_Room:
    def __init__(self, id: int, capacity: int, room: type_of_room):
        self.id = id
        self.capacity = capacity
        self.room = room
    def __str__(self):
        return f"Room ID: {self.id}, Capacity: {self.capacity}, Type: {self.room}"

#about d'une nouvelle réservation de salle

class Reserve_a_room:
    def __init__(self, id: int, date: int, début: int, fin: int, client: Nouveau_Client, salle_dispo: Nouvelle_Salle):
        self.id = id
        self.date = date
        self.début = début
        self.fin = fin
        self.client = client
        self.salle_dispo = salle_dispo
    def __str__(self):
        return f"Reservation ID: {self.id}, Date: {self.fin}, Time: {self.fin}, Client: {self.client}, Room: {self.salle_dispo}"
    
#Information sur la réservation
class Reservation:
    def __init__(self, msg: str, client: Nouveau_Client, début: Reserver_une_salle, fin: Reserver_une_salle, durée: int, salle: Nouvelle_Salle, capacité: Nouvelle_Salle):
        self.capacité = capacité
        self.salle = salle
        self.durée = durée
        self.msg = msg
        self.client = client
        self.début = début
        self.fin = fin
    def __str__(self):  
        return f"Reservation: {self.msg}, Client: {self.client}, Start: {self.début}, End: {self.fin}, Duration: {self.durée} hours, Room: {self.salle}, Capacity: {self.capacité}"
    

#Affichage d'informations
#class Afficher_les_informations:
    

