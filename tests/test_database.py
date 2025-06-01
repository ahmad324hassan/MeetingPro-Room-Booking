import src.database
from src.database import Database
from src.customers import New_Customer
from src.room import New_Room, type_of_room
from src.reservation import Reserve_a_room
import pytest
import tempfile




def create_database():
    tmp = tempfile.NamedTemporaryFile(delete=False) #add delete=False to keep the file after closing
    return Database(filepath=tmp.name)



def test_add_customer():
    db = create_database()
    customer = {"name": "Ahmad", "surname": "Hassan", "email": "ahmad.hassan@uha.fr", "id_customer": "1troll1"}
    customer_obj = New_Customer(**customer)
    db.add_customer(customer_obj)
    assert len(db.get_customers()) == 1

def test_add_room():
    db = create_database()
    room_type = type_of_room(Standard="Yes", Conference="No", Informatics="No")
    room = New_Room(id="R1", capacity=4, room=room_type)
    db.add_room(room)
    assert len(db.get_rooms()) == 1

def test_add_reservation():
    db = create_database()
    customer = New_Customer(name="Ahmad", surname="Hassan", email="ahmad.hassan@uha.fr", id_customer="1troll1")
    db.add_customer(customer)
    room_type = type_of_room(Standard="Yes", Conference="No", Informatics="No")
    room = New_Room(id="R1", capacity=4, room=room_type)
    db.add_room(room)
    assert len(db.get_rooms()) == 1


def test_get_customers():
    db = create_database()
    customer = New_Customer(name="Ahmad", surname="Hassan", email="ahmad.hassan@uha.fr", id_customer="1troll1")
    db.add_customer(customer)       
    customers = db.get_customers()
    assert len(customers) == 1

def test_get_rooms():
    db = create_database()
    room_type = type_of_room(Standard="Yes", Conference="No", Informatics="No")
    room = New_Room(id="R1", capacity=4, room=room_type)
    db.add_room(room)
    rooms = db.get_rooms()
    assert len(rooms) == 1

def test_get_reservations():
    db = create_database()
    customer = New_Customer(name="Ahmad", surname="Hassan", email="ahmad.hassan@uha.fr", id_customer="1troll1")
    db.add_customer(customer)
    room_type = type_of_room(Standard="Yes", Conference="No", Informatics="No") 
    room = New_Room(id="R1", capacity=4, room=room_type)
    db.add_room(room)
    assert len(db.get_rooms()) == 1



                            









