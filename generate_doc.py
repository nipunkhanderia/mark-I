from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ── helpers ──────────────────────────────────────────────────────────────────

def title(text):
    p = doc.add_heading(text, level=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def h1(text):
    doc.add_heading(text, level=1)

def h2(text):
    doc.add_heading(text, level=2)

def body(text):
    doc.add_paragraph(text)

def bullet(text):
    doc.add_paragraph(text, style="List Bullet")

def code(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Courier New"
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x1F, 0x7A, 0x1F)   # dark green

def divider():
    doc.add_paragraph("─" * 70)

# ── COVER ─────────────────────────────────────────────────────────────────────

title("Python & QA — Core Concepts Guide")
body("This document covers every concept in the mark-I learning project.\n"
     "Read it alongside the code files for the best understanding.")
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 1. PYTEST BASICS
# ══════════════════════════════════════════════════════════════════════════════
h1("1. What is pytest?")
body(
    "pytest is a Python testing framework. You write small functions whose names "
    "start with 'test_', and pytest finds and runs them automatically. "
    "If no exception is raised, the test passes. If an assertion fails or an "
    "exception is raised, the test fails."
)
h2("Basic test example")
code(
    "def test_addition():\n"
    "    assert 1 + 1 == 2   # passes — no exception raised\n\n"
    "def test_subtraction():\n"
    "    assert 5 - 3 == 99  # FAILS — AssertionError is raised"
)
h2("How to run tests")
code(
    "pytest -v        # -v = verbose, shows each test name\n"
    "pytest -v -s     # -s = show print() output in terminal"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 2. FIXTURES
# ══════════════════════════════════════════════════════════════════════════════
h1("2. Fixtures — Reusable Setup Code")
body(
    "A fixture is a function decorated with @pytest.fixture. "
    "Instead of copying setup code into every test, you write it once as a fixture "
    "and pytest automatically injects it into any test that lists it as a parameter."
)
body(
    "Think of a fixture like a waiter who prepares your table before you sit down "
    "and clears it after you leave — you don't have to do it yourself."
)
h2("Without fixtures (bad — repeated setup)")
code(
    "def test_one():\n"
    "    counter = Counter()   # setup repeated\n"
    "    counter.increment()\n"
    "    assert counter.value == 1\n\n"
    "def test_two():\n"
    "    counter = Counter()   # setup repeated again\n"
    "    assert counter.value == 0"
)
h2("With fixtures (good — setup written once)")
code(
    "@pytest.fixture\n"
    "def fresh_counter():\n"
    "    return Counter()      # written once, reused everywhere\n\n"
    "def test_one(fresh_counter):   # pytest injects the fixture automatically\n"
    "    fresh_counter.increment()\n"
    "    assert fresh_counter.value == 1\n\n"
    "def test_two(fresh_counter):\n"
    "    assert fresh_counter.value == 0"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 3. YIELD VS RETURN IN FIXTURES
# ══════════════════════════════════════════════════════════════════════════════
h1("3. yield vs return in Fixtures")
body(
    "This is one of the most important pytest concepts. "
    "Both 'return' and 'yield' give a value to the test, but 'yield' also lets "
    "you write cleanup code that runs AFTER the test finishes — even if the test fails."
)

h2("return — no cleanup possible")
body("Use 'return' when your fixture creates something that does not need to be cleaned up.")
code(
    "@pytest.fixture\n"
    "def simple_numbers():\n"
    "    return {'a': 10, 'b': 5}   # gives dict to test, then fixture is done\n\n"
    "# Timeline:\n"
    "# 1. fixture runs → returns dict\n"
    "# 2. test runs\n"
    "# 3. nothing else happens"
)

h2("yield — setup + teardown in one function")
body("Use 'yield' when your fixture creates something that MUST be cleaned up (e.g. a database connection, a file, a counter).")
code(
    "@pytest.fixture\n"
    "def fresh_counter():\n"
    "    counter = Counter()          # SETUP — runs before the test\n"
    "    print('Counter created')\n\n"
    "    yield counter                # test runs HERE, counter is passed to test\n\n"
    "    counter.reset()              # TEARDOWN — runs after the test\n"
    "    print('Counter reset')\n\n"
    "# Timeline:\n"
    "# 1. setup code runs (before yield)\n"
    "# 2. counter is handed to the test\n"
    "# 3. test runs\n"
    "# 4. teardown code runs (after yield) — even if test failed!"
)

h2("Key difference summary")
bullet("return  →  setup only, no cleanup")
bullet("yield   →  setup before yield, cleanup after yield")
bullet("yield teardown runs even when the test crashes — return cannot do this")
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 4. CONFTEST.PY
# ══════════════════════════════════════════════════════════════════════════════
h1("4. conftest.py — Shared Fixture Hub")
body(
    "conftest.py is a special file that pytest loads automatically before running "
    "any tests. Fixtures defined inside it are available to ALL test files in the "
    "same folder — no import statement needed."
)
body(
    "Think of conftest.py as a communal kitchen. Every test file can use what's "
    "in it without having to bring their own ingredients."
)
h2("Rules")
bullet("File must be named exactly: conftest.py")
bullet("Place it in the same folder as your test files")
bullet("No import needed in test files — pytest finds fixtures automatically")
bullet("You can have multiple conftest.py files in nested folders for different scopes")

h2("Fixture scopes — how often a fixture is created")
body("The 'scope' parameter controls how many times pytest creates and destroys a fixture.")
code(
    "@pytest.fixture(scope='function')   # DEFAULT — new fixture for every test\n"
    "@pytest.fixture(scope='module')     # one fixture for the whole test file\n"
    "@pytest.fixture(scope='session')    # one fixture for the entire test run"
)
body("Use scope='module' or scope='session' for slow setup like database connections, so you don't pay the setup cost for every single test.")
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 5. PARAMETRIZE
# ══════════════════════════════════════════════════════════════════════════════
h1("5. @pytest.mark.parametrize — One Test, Many Inputs")
body(
    "Instead of writing the same test three times with different numbers, "
    "parametrize lets you write it once and supply a table of inputs. "
    "pytest runs the test once per row."
)
h2("Without parametrize (bad — duplicated tests)")
code(
    "def test_add_1_2(): assert add(1, 2) == 3\n"
    "def test_add_0_0(): assert add(0, 0) == 0\n"
    "def test_add_neg():  assert add(-1, 1) == 0"
)
h2("With parametrize (good — one test, three runs)")
code(
    "@pytest.mark.parametrize('a, b, expected', [\n"
    "    (1,  2, 3),\n"
    "    (0,  0, 0),\n"
    "    (-1, 1, 0),\n"
    "])\n"
    "def test_add(a, b, expected):\n"
    "    assert add(a, b) == expected\n\n"
    "# pytest runs this as:\n"
    "#   test_add[1-2-3]    PASSED\n"
    "#   test_add[0-0-0]    PASSED\n"
    "#   test_add[-1-1-0]   PASSED"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 6. TESTING EXCEPTIONS
# ══════════════════════════════════════════════════════════════════════════════
h1("6. Testing Exceptions with pytest.raises()")
body(
    "Sometimes the correct behaviour is for your code to raise an error. "
    "pytest.raises() lets you assert that the right exception is raised "
    "with the right message."
)
code(
    "def test_divide_by_zero():\n"
    "    with pytest.raises(ValueError, match='Cannot divide by zero'):\n"
    "        divide(10, 0)   # this MUST raise ValueError, otherwise test fails\n\n"
    "# If divide(10, 0) raises ValueError  → test PASSES\n"
    "# If divide(10, 0) raises nothing     → test FAILS\n"
    "# If divide(10, 0) raises TypeError   → test FAILS (wrong exception type)"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 7. MULTITHREADING
# ══════════════════════════════════════════════════════════════════════════════
h1("7. Multithreading in Python")
body(
    "A thread is a unit of execution inside a program. Multithreading means "
    "running multiple threads at the same time inside the same process. "
    "Threads share the same memory, which makes them fast to create but "
    "requires care when they write to the same variable."
)
h2("Creating and running threads")
code(
    "import threading\n\n"
    "def my_task():\n"
    "    print('task running')\n\n"
    "t = threading.Thread(target=my_task)  # create thread\n"
    "t.start()                              # start it\n"
    "t.join()                               # wait for it to finish"
)
h2("Race condition — the danger of shared state")
body(
    "A race condition happens when two threads read and write the same variable "
    "at the same time, producing an unpredictable result."
)
code(
    "counter = 0\n\n"
    "def increment():\n"
    "    global counter\n"
    "    counter += 1   # NOT safe — two threads can collide here\n\n"
    "# Fix: use a Lock\n"
    "lock = threading.Lock()\n\n"
    "def safe_increment():\n"
    "    with lock:         # only one thread runs this block at a time\n"
    "        counter += 1   # now safe"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 8. THE PYTHON GIL
# ══════════════════════════════════════════════════════════════════════════════
h1("8. The Python GIL (Global Interpreter Lock)")
body(
    "The GIL is a lock inside the Python interpreter that allows only ONE thread "
    "to execute Python code at a time, even on a machine with multiple CPU cores. "
    "It exists to protect Python's internal memory management from corruption."
)
h2("What the GIL means in practice")
bullet("Threads in Python do NOT run truly in parallel for CPU work")
bullet("Only one thread runs Python bytecode at any moment")
bullet("The GIL is RELEASED when a thread is waiting (sleeping, reading a file, network call)")

h2("I/O-bound work — threads DO help")
body(
    "When a thread is waiting for a network response or a file to load, "
    "it releases the GIL. Other threads can run during that wait. "
    "This is why threads speed up I/O-bound programs."
)
code(
    "# 5 threads each sleep 0.05s\n"
    "# Without threads: 5 × 0.05 = 0.25s total\n"
    "# With threads:    all sleep at the same time ≈ 0.05s total  ← faster!"
)

h2("CPU-bound work — threads do NOT help")
body(
    "If your code is doing heavy calculations (no waiting), the GIL stays locked "
    "and threads take turns one at a time — no speedup. "
    "Use multiprocessing instead, because each process has its own GIL."
)
code(
    "# For CPU-bound work:\n"
    "from concurrent.futures import ProcessPoolExecutor\n\n"
    "with ProcessPoolExecutor() as executor:\n"
    "    results = list(executor.map(heavy_calculation, inputs))"
)

h2("Quick reference")
bullet("I/O-bound (network, file, sleep)  →  use threading")
bullet("CPU-bound (calculations, loops)   →  use multiprocessing")
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 9. PARALLEL TEST EXECUTION — pytest-xdist
# ══════════════════════════════════════════════════════════════════════════════
h1("9. Parallel Test Execution with pytest-xdist")
body(
    "pytest-xdist is a plugin that runs your tests across multiple CPU cores at "
    "the same time. It does this by spawning separate worker PROCESSES (not threads), "
    "so each worker has its own GIL — giving true parallelism."
)
h2("How to use it")
code(
    "pip install pytest-xdist\n\n"
    "pytest -n auto    # auto = one worker per CPU core\n"
    "pytest -n 4       # exactly 4 workers"
)
h2("Rules for parallel-safe tests")
bullet("Tests must be independent — no test should rely on another test's result")
bullet("No shared mutable variables at module level")
bullet("Each test must set up its own data (use fixtures)")
body(
    "If test A writes to a global variable and test B reads it, running them in "
    "parallel will produce random failures because the order is no longer guaranteed."
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 10. AI AGENT CONTEXT MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
h1("10. AI Agent Context Management")
body(
    "An AI agent is a program that uses a Large Language Model (LLM) to decide "
    "what action to take next. The agent works in a loop: it reads some input, "
    "decides what to do, does it, reads the result, and repeats."
)
h2("What is a context window?")
body(
    "The context window is the agent's short-term memory — the list of messages "
    "it can 'see' when making a decision. Every message (user input, tool result, "
    "agent response) takes up space in this window."
)
body(
    "LLMs have a maximum token limit. When the context grows too large, old messages "
    "must be dropped or summarised to make room for new ones."
)
h2("The observe → plan → act cycle")
body("Every QA agent action follows this three-step loop:")
bullet("Observe  — read the test output or environment state")
bullet("Plan     — decide what action to take based on what was observed")
bullet("Act      — execute the action and record the result in context")
code(
    "agent.observe('test_login FAILED: AssertionError')\n"
    "action = agent.plan()    # returns 'investigate_failure'\n"
    "result = agent.act(action)"
)
h2("Context trimming")
body(
    "When the history list grows beyond max_steps, the oldest messages are removed. "
    "Real production agents summarise old messages instead of deleting them, "
    "so important information is not lost."
)
code(
    "def _trim(self):\n"
    "    if len(self.history) > self.max_steps:\n"
    "        self.history = self.history[-self.max_steps:]  # keep only latest N"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# 11. REPOSITORY-LEVEL INSTRUCTIONS
# ══════════════════════════════════════════════════════════════════════════════
h1("11. Repository-Level Instructions for Coding Agents")
body(
    "When you use an AI coding assistant (like Amazon Q) in a team project, "
    "different developers might get different code styles from the AI. "
    "Repository-level instructions solve this by giving the AI a rulebook "
    "that applies to every request in that project."
)
h2("How it works in this project")
body(
    "The file .amazonq/rules/engineering_standards.md is automatically loaded "
    "by Amazon Q for every chat message in this workspace. "
    "It tells the AI: use Python 3.10+, follow PEP 8, always use yield fixtures "
    "for cleanup, never use bare except, and so on."
)
h2("Why this matters for QA")
bullet("Ensures every AI-generated test follows the same fixture patterns")
bullet("Prevents the AI from introducing shared mutable state in tests")
bullet("Enforces the observe → plan → act pattern for agent tests")
bullet("Makes code reviews easier — everyone (human and AI) follows the same rules")

h2("Example rule from engineering_standards.md")
code(
    "## Testing Standards\n"
    "- Use yield fixtures when teardown/cleanup is needed\n"
    "- Use scope='module' for fixtures that are slow to create\n"
    "- Tests must be independent — no test should depend on another test\n"
    "- Use pytest.mark.parametrize instead of writing duplicate tests"
)
divider()

# ══════════════════════════════════════════════════════════════════════════════
# QUICK REFERENCE CARD
# ══════════════════════════════════════════════════════════════════════════════
h1("Quick Reference Card")

h2("pytest commands")
code(
    "pytest -v -s              # run all tests, verbose + print output\n"
    "pytest test_math_utils.py # run one file only\n"
    "pytest -k 'counter'       # run tests whose name contains 'counter'\n"
    "pytest -n auto            # run in parallel (requires pytest-xdist)"
)

h2("Fixture scope cheat sheet")
code(
    "scope='function'  → new fixture per test          (default)\n"
    "scope='module'    → one fixture per test file\n"
    "scope='session'   → one fixture for entire run"
)

h2("yield fixture template")
code(
    "@pytest.fixture\n"
    "def my_fixture():\n"
    "    # --- SETUP ---\n"
    "    resource = create_something()\n\n"
    "    yield resource   # test runs here\n\n"
    "    # --- TEARDOWN ---\n"
    "    resource.close()"
)

h2("GIL cheat sheet")
code(
    "I/O-bound (sleep, network, file)  →  threading      (GIL released while waiting)\n"
    "CPU-bound (calculations)          →  multiprocessing (each process has own GIL)"
)

h2("Agent workflow template")
code(
    "agent.observe(test_output)   # step 1: read environment\n"
    "action = agent.plan()        # step 2: decide what to do\n"
    "result  = agent.act(action)  # step 3: do it, log result"
)

# ── save ──────────────────────────────────────────────────────────────────────
doc.save("Python_QA_Concepts.docx")
print("Done — Python_QA_Concepts.docx created.")
