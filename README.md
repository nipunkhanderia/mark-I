# mark-I — Python & QA Learning Project

## Setup
```bash
pip install -r requirements.txt
```

## Run all tests
```bash
pytest -v -s
```

## Run tests in parallel (pytest-xdist)
```bash
pytest -n auto -v
```

---

## What each file teaches

| File | Gap it covers |
|---|---|
| `math_utils.py` | App code to test against |
| `conftest.py` | Shared fixtures, `yield` vs `return`, fixture scopes |
| `test_math_utils.py` | Fixtures, parametrize, exception testing |
| `test_parallel.py` | Multithreading, the GIL, parallel test execution |
| `test_ai_agent.py` | AI agent context management, QA agent workflows |
| `.amazonq/rules/engineering_standards.md` | Repo-level instructions for coding agents |

---

## Key concepts at a glance

### yield vs return in fixtures
- `return` — gives value to test, no cleanup possible
- `yield` — gives value to test, code after `yield` runs as teardown (even on failure)

### The Python GIL
- Only ONE thread runs Python code at a time
- Threads still help for I/O-bound work (network, file, sleep) because the GIL is released while waiting
- For CPU-bound work, use `multiprocessing` instead

### Parallel tests with pytest-xdist
- `pytest -n auto` spawns one worker process per CPU core
- Each process has its own GIL — true parallelism
- Tests must be independent (no shared mutable state)

### AI Agent Context Management
- An agent carries a "context window" — its memory of past steps
- When context grows too large, old messages are trimmed or summarized
- QA agents follow: observe (read test output) → plan (decide action) → act (execute)

### Repository-level instructions
- `.amazonq/rules/engineering_standards.md` is loaded automatically by Amazon Q
- It tells the coding agent the rules for THIS repo (style, testing, agent standards)
- This is how teams enforce consistency when using AI coding assistants
