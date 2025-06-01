from src.reservation import Reserve_a_room
import pytest

def create_reservation():
    return Reserve_a_room(
        room_id=1,
        id_customer="1troll1",
        date="2025-06-01",
        debut="09:00",
        fin="17:00",
        id_reservation="res123"
    )

