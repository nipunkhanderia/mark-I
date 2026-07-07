


import pytest

@pytest.fixture
def db_connection():
    return "DB is connected"

def test_db_connection(db_connection):
    conection = db_connection
    print (conection)

@pytest.fixture
def db_y_connection():
    yield "DB is yielded"


def test_y_db(db_y_connection):
    connn = db_y_connection 
    print(connn)

test_db_connection
test_y_db
