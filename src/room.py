class type_of_room:
    def __init__(self, Standard: str, Conference: str, Informatics: str):
        self.Standard = Standard
        self.Conference = Conference
        self.Informatics = Informatics    
    def __str__(self):  
        return f"Room Types: Standard: {self.Standard}, Conference: {self.Conference}, IT: {self.Informatics}"
    


class New_Room:
    def __init__(self, id: int, capacity: int, room: type_of_room):
        self.id = id
        self.capacity = capacity
        self.room = room
    def __str__(self):
        return f"Room ID: {self.id}, Capacity: {self.capacity}, Type: {self.room}"
    

    def room_infos(self):   
        return {
            "id": self.id,
            "capacity": self.capacity,
            "room_type": {
                "Standard": self.room.Standard,
                "Conference": self.room.Conference,
                "Informatics": self.room.Informatics
            }
        }