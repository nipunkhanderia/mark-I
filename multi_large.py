# multi_large.py
# 20 slow tests — this is where parallel execution shines
import time
import pytest

@pytest.mark.parametrize("i", range(20))
def test_slow_task(i):
    time.sleep(1)  # simulates a slow API call or DB query
    assert i >= 0
