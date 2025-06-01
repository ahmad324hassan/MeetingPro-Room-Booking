import json
import uuid
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
        self.save() # Save the updated data to the JSON file (function defined below)

    def add_room(self, room: room.New_Room): # This function adds a new room to the database
        for r in self.data['rooms']:
            if r['id'] == room.id: # Check if the room already exists in the database and raise an error if it does
                raise ValueError("This room already exists.")
        self.data['rooms'].append(room.room_infos()) # Add the room information to the database if it doesn't already exist
        self.save()

    def add_reservation(self, reservation: reservation.Reserve_a_room): # This function adds a new reservation to the database
        reservation_id = getattr(reservation, "id_reservation", None) # Get the reservation ID if it exists, otherwise set it to None
        if not reservation_id:
            reservation.id_reservation = str(uuid.uuid4())#if no ID exists, generate a new unique ID for the reservation
        for r in self.data['reservations']:
            if r.get('id', None) == reservation.id_reservation:
                raise ValueError("This reservation already exists.") # Check if the reservation already exists in the database and raise an error if it does
        res_dict = reservation.reservation_infos()
        if 'id' not in res_dict:
            res_dict['id'] = reservation.id_reservation #If the reservation ID is not in the dictionary, add it
        self.data['reservations'].append(res_dict)
        self.save()


    # Save the current state of the database to the JSON file
    def save(self):
        with open(self.filepath, 'w') as file: # Save the JSON data to the file
            json.dump(self.data, file, indent=4) # Ensure that the JSON is pretty-printed


    # Getters for customers, rooms, and reservations

    def get_customers(self): # This function retrieves the list of customers from the database
        customers_list = []
        for c in self.data['customers']:
            if 'id' in c:
                c = c.copy()
                c['id_customer'] = c.pop('id')
            customers_list.append(customers.New_Customer(**c))
        return customers_list

    def get_rooms(self): # This function retrieves the list of rooms from the database
        rooms_list = []
        for r in self.data['rooms']:
            r = r.copy()
            if 'room_type' in r:
                r['room'] = r.pop('room_type')
            from room import type_of_room
            if isinstance(r['room'], dict): # If the room is a dictionary, convert it to a type_of_room object
                r['room'] = type_of_room(
                    Standard=r['room'].get('Standard', 'No'),
                    Conference=r['room'].get('Conference', 'No'),
                    Informatics=r['room'].get('Informatics', 'No')
                )
            rooms_list.append(room.New_Room(**r)) # Create a New_Room object with the room data
        return rooms_list

    def get_reservations(self): # This function retrieves the list of reservations from the database
        reservations_list = []
        for r in self.data['reservations']:
            r = r.copy()
            id_reservation = r.pop('id', None)# If the reservation has an ID, remove it from the dictionary
            reservations_list.append( # Create a Reserve_a_room object with the reservation data
                reservation.Reserve_a_room(
                    r['room_id'],
                    r['id_customer'],
                    r['date'],
                    r['debut'],
                    r['fin'],
                    id_reservation=id_reservation
                )
            )
        return reservations_list

