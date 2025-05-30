import uuid

class New_Customer:
    def __init__(self, name: str, surname: str, email: str, id_customer: str = None):
        self.id_customer = id_customer or str(uuid.uuid4())
        self.name = name
        self.surname = surname
        self.email = email
    def __str__(self):
        return f"Client: {self.name} {self.surname}, Email: {self.email}, ID: {self.id_customer}"

    def customer_infos(self):
        return {
            "id": self.id_customer,
            "name": self.name,
            "surname": self.surname,
            "email": self.email
        }   


