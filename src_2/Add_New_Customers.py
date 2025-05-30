import json 
from uuid import uuid4


list_of_customers = [] # This will hold the list of customers
NewCustomer = Class.New_Customer

def add_new_customers(list_of_customers, NewCustomer):

    for customer in list_of_customers:
        if customer.name == NewCustomer.name and customer.surname == NewCustomer.surname and customer.email == NewCustomer.email and customer.id == NewCustomer.id:
            # If the customer already exists, print an error message
            raise ValueError("This customer already exists.")
        elif customer.name != NewCustomer.name or customer.surname != NewCustomer.surname or customer.email != NewCustomer.email or customer.id != NewCustomer.id:
            # If the customer does not exist, add it to the list
            list_of_customers.append(NewCustomer)
            # If the customer is added successfully, write it to the JSON file
            print("Customer added successfully.")       
            NewCustomer.id = str(uuid4())
            NewCustomer = {
                "id": NewCustomer.id,
                "name": NewCustomer.name,
                "surname": NewCustomer.surname,
                "email": NewCustomer.email
            }
"""
            with open("utilisateurs.json", "a") as fichier:
                fichier.write(json.dumps(NewCustomer) + "\n")"""