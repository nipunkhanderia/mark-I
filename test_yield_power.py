import pytest


# --- RETURN fixture: no cleanup possible ---
@pytest.fixture
def db_connection():
    print("\n[RETURN] Connecting to DB...")
    return "DB is connected"
    # Nothing can run after return — if the test leaves a mess, too bad.


def test_db_connection(db_connection):
    print(f"  Using: {db_connection}")
    # Imagine this test corrupts the DB — no automatic cleanup happens.


# --- YIELD fixture: setup + automatic teardown ---
@pytest.fixture
def db_y_connection():
    print("\n[YIELD SETUP] Connecting to DB...")
    connection = "DB is yielded"

    yield connection  # test runs here

    # This runs AFTER the test — even if the test FAILS or crashes
    print("[YIELD TEARDOWN] Closing DB connection... cleaned up!")


def test_y_db_passes(db_y_connection):
    print(f"  Using: {db_y_connection}")
    assert True  # test passes — teardown still runs


def test_y_db_fails(db_y_connection):
    print(f"  Using: {db_y_connection}")
    assert False, "Oops I crashed!"  # test FAILS — teardown STILL runs!
