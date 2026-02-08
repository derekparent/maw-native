# MAW Test Fixture

A minimal Python project with intentional issues for testing MAW Native's multi-agent workflow.

## Known Issues (for agents to find and fix)

- `src/calculator.py` — Division by zero bug, empty list bug
- `src/auth.py` — Missing input validation, plaintext passwords, no authorization checks
- `src/utils.py` — No type hints, no docstrings
- `tests/test_calculator.py` — Missing edge case tests, no tests for auth or utils

## Running Tests

```bash
pytest -v
```
