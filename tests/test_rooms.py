from src.room import New_Room, type_of_room
import pytest

def test_create_New_Room():
    room = New_Room(1, 10, type_of_room(Standard="Yes", Conference="No", Informatics="No"))
    assert room.id == 1
    assert room.capacity == 10
    assert room.room.Standard == "Yes"
