---
applyTo: "**/*.py"
description: "Use when writing, reviewing, or modifying Python code. Covers style, typing, project structure, and common patterns."
---
# Python Coding Standards

## Style
- Follow PEP 8 for formatting and naming conventions
- Use `snake_case` for functions, methods, and variables; `PascalCase` for classes
- Prefer f-strings over `.format()` or `%` formatting
- Use trailing commas in multi-line collections and function signatures

## Type Hints
- Add type hints to all function signatures (parameters and return types)
- Use modern syntax: `list[str]`, `dict[str, int]`, `str | None` (not `Optional[str]`)
- Use `from __future__ import annotations` when targeting Python <3.10

## Imports
- Group imports: stdlib → third-party → local, separated by blank lines
- Use absolute imports over relative imports
- Avoid wildcard imports (`from module import *`)

## Functions & Classes
- Keep functions short and focused on a single responsibility
- Use keyword arguments for functions with more than 2-3 parameters
- Prefer dataclasses or named tuples over plain dicts for structured data
- Use `@staticmethod` or `@classmethod` where appropriate

## Error Handling
- Catch specific exceptions, never bare `except:`
- Use context managers (`with` statements) for resource management
- Raise exceptions with clear, descriptive messages

## Testing
- Write tests using `pytest` conventions
- Name test files `test_<module>.py` and test functions `test_<behavior>`
- Use fixtures for shared setup; prefer factory functions over complex fixtures
