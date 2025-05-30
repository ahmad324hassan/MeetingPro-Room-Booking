import tkinter as tk

from src.database import Database

from src.customers  import New_Customer
from src.room import New_Room
from src.reservation import Reserve_a_room


if __name__ == "__main__":
    db = Database("data.json")  # Initialize the database with a file path


