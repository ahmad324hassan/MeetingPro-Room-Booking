from src.customers import New_Customer
import pytest

def test_create_New_Customer():
    customer = New_Customer(name="Bismuth", surname="Dorian", email="dorian.bismuth@uha.fr", id_customer="1troll1")
    assert customer.name == "Bismuth"
    assert customer.surname == "Dorian"
    assert customer.email == "dorian.bismuth@uha.fr"
    assert customer.id_customer == "1troll1"
