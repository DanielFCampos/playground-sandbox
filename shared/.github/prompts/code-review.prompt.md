---
description: "Review code for clean code violations, bugs, and improvement opportunities. Use on files, selections, or PRs."
---
Review the provided code using the checklist below. For each issue found, state the category, location, what's wrong, and a concrete fix.

## Checklist

### Naming
- [ ] Are names intention-revealing and consistent?
- [ ] Are booleans named as questions (`is_*`, `has_*`, `should_*`)?
- [ ] Are there abbreviations or ambiguous names?

### Functions
- [ ] Is each function focused on a single task?
- [ ] Are there functions with more than 3 parameters that should use an object/data structure?
- [ ] Can nesting be reduced with early returns or guard clauses?
- [ ] Are there flag arguments that split a function into two behaviors?

### Simplicity
- [ ] Is there dead code, commented-out code, or unused imports?
- [ ] Is there speculative generality or premature abstraction?
- [ ] Is there real duplication that should be extracted?

### Readability
- [ ] Does the code read top-down?
- [ ] Are comments explaining *what* instead of *why*?
- [ ] Are files focused on a single concept?

### Error Handling
- [ ] Are errors handled explicitly and close to the source?
- [ ] Are exceptions swallowed without logging or re-raising?
- [ ] Are resources properly cleaned up (context managers, `finally`, etc.)?

### Dependencies
- [ ] Is there unnecessary coupling between modules?
- [ ] Are public APIs minimal and intentional?
- [ ] Are there circular dependencies?

### Bugs & Security
- [ ] Are there potential null/undefined access errors?
- [ ] Is user input validated at system boundaries?
- [ ] Are there injection risks (SQL, XSS, command)?

## Output Format

If no issues are found, say "Looks clean — no issues found."

Otherwise, list issues as:

**[Category] file:line** — description of the problem.
→ Suggested fix or refactored code.
