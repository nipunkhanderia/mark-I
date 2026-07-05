# Engineering Standards
# This file is automatically read by Amazon Q (and other coding agents) for
# every request in this repo. It tells the agent HOW to write code here.
# This is what "repository-level instructions" means in a coding-agent workflow.

## Python Style
- Use Python 3.10+
- Follow PEP 8: snake_case for functions/variables, PascalCase for classes
- Keep functions under 20 lines; split if longer
- No bare `except:` — always catch a specific exception type

## Testing Standards
- Every new function in math_utils.py must have at least one test
- Use pytest fixtures from conftest.py — do not repeat setup code in tests
- Use `yield` fixtures when teardown/cleanup is needed
- Use `scope="module"` for fixtures that are slow to create (e.g. DB connections)
- Tests must be independent — no test should depend on another test's side effects
- Use `pytest.mark.parametrize` instead of writing duplicate tests

## AI Agent Workflow Standards
- AgentContext.max_steps must always be set explicitly — never rely on defaults
- Every agent action must be logged to context before returning
- Agent tests must cover: observe → plan → act cycle end-to-end

## Parallel Execution
- All tests must be stateless and safe to run with `pytest -n auto`
- Never use module-level mutable variables in tests
