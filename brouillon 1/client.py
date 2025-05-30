class New_Customer:
    def __init__(self, name: str, surname: str, email: str, id: str):
        self.id = str(uuid4())
        self.name = name
        self.surname = surname
        self.email = email
    def __str__(self):
        return f"Client: {self.name} {self.surname}, Email: {self.email}, ID: {self.id}"
    
