"""
Demonstrates the real advantage of `yield` over `return` in pytest fixtures:
guaranteed teardown -> test isolation, regardless of pass/fail/order.

Run with:  pytest test_return_vs_yield.py -v -s
"""
import pytest


# ======================================================================
# BAD: return-based fixture -> no teardown -> state leaks between tests
# ======================================================================
shared_db_return = []

@pytest.fixture
def db_return():
    # No teardown possible. Function ends at 'return'.
    return shared_db_return


def test_add_user_return(db_return):
    db_return.append("alice")
    assert len(db_return) == 1          # PASSES


def test_add_another_user_return(db_return):
    db_return.append("bob")
    # This test assumes a clean db with only "bob" in it.
    assert len(db_return) == 1          # FAILS -> ['alice', 'bob'], alice leaked in


# ======================================================================
# GOOD: yield-based fixture -> guaranteed teardown -> isolated tests
# ======================================================================
shared_db_yield = []

@pytest.fixture
def db_yield():
    yield shared_db_yield               # test runs here
    shared_db_yield.clear()             # teardown: ALWAYS runs after, pass or fail


def test_add_user_yield(db_yield):
    db_yield.append("alice")
    assert len(db_yield) == 1           # PASSES


def test_add_another_user_yield(db_yield):
    db_yield.append("bob")
    assert len(db_yield) == 1           # PASSES -> teardown cleared "alice" already