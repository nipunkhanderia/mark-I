# conftest.py
# pytest automatically loads this file before running any tests.
# Fixtures defined here are SHARED across ALL test files — no import needed.

import pytest
from math_utils import Counter

# --- FIXTURE WITH RETURN ---
@pytest.fixture
def simple_numbers():
    # "return" gives the value to the test, then fixture is done.
    # Use this when there is NO cleanup needed after the test.
    return {"a": 10, "b": 5}

# --- FIXTURE WITH YIELD (the important one) ---
@pytest.fixture
def fresh_counter():
    # Everything BEFORE yield = setup (runs before the test)
    counter = Counter()
    print("\n[SETUP] Counter created")

    yield counter  # <-- hands the counter to the test; test runs here

    # Everything AFTER yield = teardown (runs after the test, even if it fails)
    counter.reset()
    print("[TEARDOWN] Counter reset to zero")

# --- SCOPED FIXTURE ---
@pytest.fixture(scope="module")
def expensive_resource():
    # scope="module" means this fixture is created ONCE for the whole file,
    # not once per test. Use for slow setup like DB connections.
    print("\n[SETUP] Expensive resource created (only once per module)")
    resource = {"connection": "fake-db-connection"}

    yield resource

    print("[TEARDOWN] Expensive resource closed")
