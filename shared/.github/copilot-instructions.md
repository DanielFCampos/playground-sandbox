---
applyTo: "**"
description: "Always-on clean code principles. Covers naming, structure, simplicity, and readability across all languages."
---
# Clean Code

## Naming
- Use intention-revealing names; a reader should understand purpose without extra context
- Avoid abbreviations and single-letter variables outside of trivial loops or lambdas
- Use consistent terminology — pick one word per concept and stick with it across the codebase
- Name booleans as questions: `is_valid`, `has_access`, `should_retry`

## Functions
- Keep functions short and focused on a single task
- Limit parameters; group related parameters into an object or data structure when there are more than 3
- Use early returns to reduce nesting and improve readability
- Avoid flag arguments that make a function do two different things

## Simplicity
- Write the simplest code that solves the problem — no speculative generality
- Remove dead code, commented-out code, and unused imports
- Prefer flat over nested: reduce indentation levels through guard clauses and extraction
- Don't repeat yourself — extract shared logic only when duplication is real, not hypothetical

## Readability
- Code should read top-down like a narrative; put high-level logic before low-level details
- Prefer self-documenting code over comments; use comments only to explain *why*, never *what*
- Keep files focused on a single concept or closely related set of concepts
- Use consistent formatting and structure across the project

## Error Handling
- Handle errors close to where they occur; don't let them propagate silently
- Prefer explicit error handling over silent defaults
- Never swallow exceptions without logging or re-raising

## Dependencies
- Minimize coupling between modules; depend on abstractions, not concrete implementations
- Keep the public API of each module small and intentional
- Avoid circular dependencies
