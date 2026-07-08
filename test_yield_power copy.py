import pytest

@pytest.fixture
def connection():
    return "Connection successful"
    print("Return----------Does it run?")


@pytest.fixture
def y_connection():
    yield "Connection succesful"
    print("---------Yield--------------Doesnt matter if the connection is success or not but this line is going to run")


def test_connection(connection):
    assert "success" in connection


def test_connection_y(y_connection):
    assert "succesful" in y_connection