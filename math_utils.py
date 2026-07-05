# math_utils.py
# This is the "app code" — the real functions we want to test.
# Keeping it simple: add, divide, and a stateful Counter class.

def add(a, b):
    return a + b  # returns the sum of two numbers

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")  # raises an error on bad input
    return a / b

class Counter:
    """A simple counter that can be incremented and reset."""

    def __init__(self):
        self.value = 0  # starts at zero

    def increment(self):
        self.value += 1  # adds 1 each time called

    def reset(self):
        self.value = 0  # puts counter back to zero
