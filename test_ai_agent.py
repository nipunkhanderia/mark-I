# test_ai_agent.py
# Covers: AI agent context management, agent memory, QA agent workflows

# ---------------------------------------------------------------------------
# WHAT IS "AI AGENT CONTEXT MANAGEMENT"?
# An AI agent is a program that uses an LLM to decide what action to take next.
# "Context" = the memory/history the agent carries between steps.
#
# In QA, an agent might:
#   1. Read a failing test
#   2. Look up related code (tool call)
#   3. Generate a fix
#   4. Run the test again to verify
#
# The agent needs to remember what it did in step 1 when it reaches step 4.
# That memory is its "context window". Managing it = deciding what to keep,
# what to summarize, and what to drop so you don't exceed the token limit.
# ---------------------------------------------------------------------------

import pytest

# --- Minimal agent simulation ---

class AgentContext:
    """Holds the agent's memory across multiple steps."""

    def __init__(self, max_steps=5):
        self.history = []       # list of {"role": ..., "content": ...} dicts
        self.max_steps = max_steps  # context window limit (simplified as step count)

    def add(self, role, content):
        # Adds a new message to context, then trims if over the limit.
        self.history.append({"role": role, "content": content})
        self._trim()

    def _trim(self):
        # Drops the oldest messages when context exceeds max_steps.
        # Real agents summarize instead of dropping — this is the simplified version.
        if len(self.history) > self.max_steps:
            self.history = self.history[-self.max_steps:]  # keep only the latest N

    def last(self):
        return self.history[-1] if self.history else None  # most recent message


class QAAgent:
    """A minimal QA agent that runs a fixed workflow using its context."""

    def __init__(self):
        self.context = AgentContext(max_steps=5)

    def observe(self, test_output):
        # Step 1: agent reads the failing test output
        self.context.add("user", f"Test output: {test_output}")

    def plan(self):
        # Step 2: agent decides what to do based on context
        last = self.context.last()
        if last and "FAILED" in last["content"]:
            action = "investigate_failure"
        else:
            action = "mark_passed"
        self.context.add("agent", f"Planned action: {action}")
        return action

    def act(self, action):
        # Step 3: agent executes the action and records the result
        result = f"Executed: {action}"
        self.context.add("agent", result)
        return result


# --- TESTS ---

def test_agent_context_stores_messages():
    ctx = AgentContext()
    ctx.add("user", "run tests")
    ctx.add("agent", "tests passed")
    assert len(ctx.history) == 2  # both messages stored

def test_agent_context_trims_old_messages():
    ctx = AgentContext(max_steps=3)
    for i in range(6):
        ctx.add("user", f"message {i}")  # add 6 messages to a window of 3
    assert len(ctx.history) == 3           # only latest 3 kept
    assert ctx.history[0]["content"] == "message 3"  # oldest kept is message 3

def test_agent_plans_investigation_on_failure():
    agent = QAAgent()
    agent.observe("test_login FAILED: AssertionError")
    action = agent.plan()
    assert action == "investigate_failure"  # agent correctly identified failure

def test_agent_plans_pass_on_success():
    agent = QAAgent()
    agent.observe("test_login PASSED")
    action = agent.plan()
    assert action == "mark_passed"  # agent correctly identified success

def test_agent_full_workflow():
    # Simulates a complete observe → plan → act cycle
    agent = QAAgent()
    agent.observe("test_checkout FAILED: timeout")
    action = agent.plan()
    result = agent.act(action)

    assert "investigate_failure" in result  # agent acted on the failure
    assert len(agent.context.history) == 3  # observe + plan + act = 3 steps

def test_agent_context_does_not_exceed_window():
    agent = QAAgent()
    # Run 10 full cycles — context must never grow beyond max_steps=5
    for i in range(10):
        agent.observe(f"test_{i} FAILED")
        action = agent.plan()
        agent.act(action)

    assert len(agent.context.history) <= 5  # context window respected
