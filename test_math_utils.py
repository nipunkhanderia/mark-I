# test_math_utils.py
# Covers: fixtures, yield vs return, conftest.py, parametrize, exception testing

import pytest
from math_utils import add, divide

# --- USING A RETURN FIXTURE (from conftest.py) ---
def test_add_with_fixture(simple_numbers):
    # pytest sees "simple_numbers" as a parameter and automatically injects
    # the fixture value — no need to import or call it yourself.
    result = add(simple_numbers["a"], simple_numbers["b"])
    assert result == 15  # 10 + 5 = 15

# --- USING A YIELD FIXTURE (from conftest.py) ---
def test_counter_increments(fresh_counter):
    # fresh_counter is the Counter object yielded by the fixture.
    # After this test finishes, conftest teardown runs automatically.
    fresh_counter.increment()
    fresh_counter.increment()
    assert fresh_counter.value == 2  # incremented twice

def test_counter_starts_fresh(fresh_counter):
    # Each test gets a BRAND NEW counter because the fixture has default
    # scope="function" — it re-runs setup/teardown for every test.
    assert fresh_counter.value == 0  # proves teardown reset it

# --- USING A MODULE-SCOPED FIXTURE (from conftest.py) ---
def test_uses_expensive_resource(expensive_resource):
    # This fixture was created once when the module started.
    assert expensive_resource["connection"] == "fake-db-connection"

def test_same_expensive_resource(expensive_resource):
    # Same object as above — setup did NOT run again. Check terminal output.
    assert expensive_resource is not None

# --- PARAMETRIZE: run one test with many inputs ---
@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),   # basic case
    (0, 0, 0),   # zeros
    (-1, 1, 0),  # negatives
])
def test_add_many_inputs(a, b, expected):
    # pytest runs this test 3 times, once per row above.
    assert add(a, b) == expected

# --- TESTING EXCEPTIONS ---
def test_divide_by_zero_raises():
    # pytest.raises() checks that the right exception is thrown.
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)  # this line should raise ValueError

def test_divide_normal():
    assert divide(10, 2) == 5.0
