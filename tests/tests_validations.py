from ..app.modules.utils import validate_table

def tests_validate_table_passeds():
    assert validate_table("") == True
    assert validate_table("") == True
    assert validate_table("") == True
    assert validate_table("") == True

def tests_validate_table_fails():
    assert validate_table("") == False
    assert validate_table("") == False
    assert validate_table("") == False
    assert validate_table("") == False
    assert validate_table("") == False
    