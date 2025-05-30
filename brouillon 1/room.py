class New_Room:
    def __init__(self, id: int, capacity: int, room: type_of_room):
        self.id = id
        self.capacity = capacity
        self.room = room
    def __str__(self):
        return f"Room ID: {self.id}, Capacity: {self.capacity}, Type: {self.room}"