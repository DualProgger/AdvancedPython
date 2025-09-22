import pytest
from main2 import DBSettings

def test_db_settings_singleton():
    db1 = DBSettings("localhost", 5432, "admin", "password123", "mydatabase")
    db2 = DBSettings("localhost", 5432, "admin", "password123", "mydatabase")
    assert db1 is db2
