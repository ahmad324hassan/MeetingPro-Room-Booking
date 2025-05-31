import json
from uuid import uuid4

import customers
import room
import reservation

# Database class to manage customers, rooms, and reservations

class Database: # This class manages the database operations for customers, rooms, and reservations
    def __init__(self, filepath: str):
        self.filepath = filepath # The path to the JSON file where the data will be stored
        self.data = {
            "customers": [],
            "rooms": [],
            "reservations": []
        }
        self.load() # Load the data from the JSON file when the class is initialized
        
    # Load the data from the JSON file
    def load(self): 
        try:
            with open(self.filepath, 'r') as file: # If the file exists, read the JSON data from it
                self.data = json.load(file) # Ensure that the file exists and is readable
        except FileNotFoundError: # Else if the file does not exist, create a new one
            self.data = {
                "customers": [],
                "rooms": [],
                "reservations": []
            }
        except json.JSONDecodeError:    # Else if there is an error decoding the JSON data, start with an empty database
            print("Error decoding JSON from the file. Starting with an empty database.")
            self.data = {
                "customers": [],
                "rooms": [],
                "reservations": []
            }

    # Methods to add new customers, rooms, and reservations
    def add_customer(self, customer: customers.New_Customer):# This method adds a new customer to the database
        for c in self.data['customers']: # Iterate through existing customers list to check for duplicates                         
            if c['id'] == customer.id_customer: # Check if the customer already exists in the database
                raise ValueError("This customer already exists.")
        self.data['customers'].append(customer.customer_infos())
        self.save()

    def add_room(self, room: room.New_Room):
        for r in self.data['rooms']:
            if r['id'] == room.id:
                raise ValueError("This room already exists.")
        self.data['rooms'].append(room.room_infos())
        self.save()

    def add_reservation(self, reservation: reservation.Reserve_a_room):
        for r in self.data['reservations']:
            if r['id'] == reservation.id_reservation:
                raise ValueError("This reservation already exists.")
        self.data['reservations'].append(reservation.reservation_infos())
        self.save()


    # Save the current state of the database to the JSON file
    def save(self):
        with open(self.filepath, 'w') as file: # Save the JSON data to the file
            json.dump(self.data, file, indent=4) # Ensure that the JSON is pretty-printed


    # Getters for customers, rooms, and reservations

    def get_customers(self):
        customers_list = []
        for c in self.data['customers']:
            if 'id' in c:
                c = c.copy()
                c['id_customer'] = c.pop('id')
            customers_list.append(customers.New_Customer(**c))
        return customers_list

    def get_rooms(self):
        rooms_list = []
        for r in self.data['rooms']:
            rooms_list.append(room.New_Room(**r))
        return rooms_list

    def get_reservations(self):
        reservations_list = []
        for r in self.data['reservations']:
            reservations_list.append(reservation.Reserve_a_room(**r))
        return reservations_list

