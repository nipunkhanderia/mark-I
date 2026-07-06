import pytest

# RETURN - fixture provides value once, no cleanup after
@pytest.fixture
def db_connection_return():
    conn = "Connected to DB"
    return conn  # function ends here, nothing runs after

# YIELD - fixture provides value, then resumes for cleanup after test finishes
@pytest.fixture
def db_connection_yield():
    conn = "Connected to DB"
    yield conn  # test runs here, using 'conn'
    print("Closing DB connection")  # this runs AFTER the test finishes

def test_using_return(db_connection_return):
    assert db_connection_return == "Connected to DB"

def test_using_yield(db_connection_yield):
    assert db_connection_yield == "Connected to DB"
    # after this test finishes, pytest resumes the yield fixture
    # and runs the cleanup code (closing connection)