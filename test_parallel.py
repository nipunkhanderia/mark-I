# test_parallel.py
# Covers: multithreading, the Python GIL, parallel test execution with pytest-xdist

import threading
import time
import pytest
from math_utils import add

# ---------------------------------------------------------------------------
# WHAT IS THE GIL?
# Python has a Global Interpreter Lock (GIL) — a mutex that allows only ONE
# thread to execute Python bytecode at a time, even on multi-core machines.
#
# GIL ALLOWS (threads still help here):
#   - I/O-bound work: file reads, network calls, sleep — thread releases GIL
#     while waiting, so other threads can run.
#
# GIL BLOCKS (threads don't help here):
#   - CPU-bound work: pure number crunching — GIL stays locked, no speedup.
#   - Use multiprocessing or concurrent.futures.ProcessPoolExecutor instead.
# ---------------------------------------------------------------------------

# --- DEMO 1: I/O-bound — threads DO help ---
def test_threads_help_with_io():
    results = []

    def fake_io_task():
        time.sleep(0.05)        # simulates waiting for network/file (GIL released)
        results.append("done")  # appends result when wait is over

    threads = [threading.Thread(target=fake_io_task) for _ in range(5)]

    start = time.time()
    for t in threads:
        t.start()   # starts all 5 threads
    for t in threads:
        t.join()    # waits for all threads to finish before moving on

    elapsed = time.time() - start

    assert len(results) == 5        # all 5 tasks completed
    assert elapsed < 0.2            # ran concurrently, not 5 × 0.05 = 0.25s sequentially

# --- DEMO 2: Thread safety — shared state needs a Lock ---
def test_shared_counter_with_lock():
    # Without a lock, multiple threads writing to the same variable can
    # cause a "race condition" — the final value becomes unpredictable.
    counter = {"value": 0}
    lock = threading.Lock()  # only one thread can hold this lock at a time

    def safe_increment():
        with lock:               # acquires lock → other threads wait here
            counter["value"] += 1  # safe: only one thread runs this at a time

    threads = [threading.Thread(target=safe_increment) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert counter["value"] == 100  # exactly 100, no lost increments

# --- DEMO 3: Parallel test execution note ---
# To run tests in parallel across CPU cores, install pytest-xdist and run:
#   pytest -n auto
#
# pytest-xdist spawns multiple worker processes (bypasses GIL because each
# process has its own GIL). Each worker runs a subset of your test suite.
# Tests must be independent — no shared mutable state between tests.

@pytest.mark.parametrize("x", range(5))
def test_independent_add(x):
    # These 5 tests have no shared state, so they are safe to run in parallel
    # with: pytest -n auto
    assert add(x, 1) == x + 1
