import json
from uuid import uuid4

import customers
import room
import reservation

# Database class to manage customers, rooms, and reservations

class Database:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = {
            "customers": [],
            "rooms": [],
            "reservations": []
        }
        self.load()
        
    def load(self): 
        try:
            with open(self.filepath, 'r') as file: # Load the JSON data from the file
                self.data = json.load(file)
        except FileNotFoundError:
            self.data = {
                "customers": [],
                "rooms": [],
                "reservations": []
            }
        except json.JSONDecodeError:    
            print("Error decoding JSON from the file. Starting with an empty database.")
            self.data = {
                "customers": [],
                "rooms": [],
                "reservations": []
            }

    # Add methods to add customers, rooms, and reservations


    def add_customer(self, customer: customers.New_Customer):
        for c in self.data['customers']:
            if c['id'] == customer.id_customer:
                raise ValueError("This customer already exists.")
        self.data['customers'].append(customer.customer_infos())
        self.save()

    def add_room(self, room: room.New_Room):
        for r in self.data['rooms']:
            if r['id'] == room.id:
                raise ValueError("This room already exists.")
        self.data['rooms'].append(room.room_infos())
        self.save()

    def add_reservation(self, reservation: reservation.New_Reservation):
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

