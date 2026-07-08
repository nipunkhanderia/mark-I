import threading
import time

def cpu_bound_task():
    count = 0
    for _ in range(50_000_000):
        count += 1

# Single-threaded
start = time.time()
cpu_bound_task()
cpu_bound_task()
print(f"Sequential: {time.time() - start:.2f}s")

# Multi-threaded (still slow due to GIL!)
start = time.time()
t1 = threading.Thread(target=cpu_bound_task)
t2 = threading.Thread(target=cpu_bound_task)
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Threaded: {time.time() - start:.2f}s")