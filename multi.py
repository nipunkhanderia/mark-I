# test_example.py
import time

def test_one():
    time.sleep(1)
    assert 1 + 1 == 2

def test_two():
    time.sleep(1)
    assert 2 + 2 == 4

def test_three():
    time.sleep(1)
    assert 3 + 3 == 6

def test_four():
    time.sleep(1)
    assert 4 + 4 == 8


#     # Sequential (takes ~4 seconds)
# pytest test_example.py

# # Parallel across 4 workers (takes ~1 second)
# pytest test_example.py -n 4