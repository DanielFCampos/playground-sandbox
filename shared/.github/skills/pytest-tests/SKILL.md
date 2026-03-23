---
name: pytest-tests
description: "Write high-quality pytest tests. Use when: creating test files, writing unit tests, integration tests, adding test coverage, mocking dependencies, testing Python functions, testing Streamlit apps, testing API integrations, testing database logic, generating conftest.py, or reviewing test quality."
argument-hint: "Describe what to test (e.g., 'test the user authentication module' or 'add tests for jobs.py')"
---

# Pytest Test Writing

Write high-quality, maintainable pytest tests that follow project conventions and testing best practices.

## When to Use

- Creating new test files for existing modules
- Adding unit or integration tests for functions/classes
- Setting up test infrastructure (conftest.py, fixtures)
- Mocking external dependencies (APIs, databases, file I/O)
- Reviewing or improving existing test quality

## Pre-flight Checks

Before writing tests:

1. **Verify pytest is installed** — check `pyproject.toml` for `pytest` in dev dependencies. If missing, add it:
   ```toml
   [dependency-groups]
   dev = [
       "pytest>=8.0.0",
       "pytest-cov>=6.0.0",
       "pytest-mock>=3.14.0",
   ]
   ```
   Then run `uv sync` to install.

2. **Check for conftest.py** — if `tests/conftest.py` doesn't exist, create it with shared fixtures (see [conftest template](./assets/conftest_template.py)).

3. **Read the source module** — understand the function signatures, return types, dependencies, and edge cases before writing tests.

## Project Conventions

Follow these rules from the project's coding standards:

| Convention | Rule |
|-----------|------|
| Test location | `tests/` directory at project root |
| File naming | `test_<module>.py` (e.g., `test_monday.py`) |
| Function naming | `test_<behavior>` (e.g., `test_get_headers_missing_api_key`) |
| Framework | `pytest` (not unittest) |
| Coverage target | At least one test per public function |
| Imports | Standard lib, then third-party, then local — alphabetical within groups |
| Type hints | Modern syntax: `list[str]`, `str | None` (not `Optional`). Only import `Any` from `typing` when needed |
| Docstrings | PEP 257 on public test helpers, not required on individual test functions |
| Line length | Enforced by `ruff` (see `pyproject.toml`) |

## Test Structure

Use the **Arrange-Act-Assert** (AAA) pattern in every test:

```python
def test_sanitize_column_name_with_spaces():
    # Arrange
    raw_name = "First Name"

    # Act
    result = _sanitize_column_name(raw_name)

    # Assert
    assert result == "first_name"
```

For simple tests, the pattern can be implicit (no comments needed):

```python
def test_sanitize_column_name_with_spaces():
    assert _sanitize_column_name("First Name") == "first_name"
```

## File Template

Every test file should follow this structure:

```python
"""Tests for <module>.py."""

import <stdlib>

import pytest
import <third_party>

from <package>.<module> import <functions_under_test>


# --- Fixtures ---

@pytest.fixture
def sample_data():
    """Provide reusable test data."""
    return {"key": "value"}


# --- Tests for <function_name> ---

class TestFunctionName:
    """Tests for function_name."""

    def test_happy_path(self):
        ...

    def test_edge_case(self):
        ...

    def test_error_handling(self):
        ...
```

### Organization Rules

- **Group tests by function** using classes (`class TestFunctionName`) or comment headers
- **Order tests**: happy path first, then edge cases, then error cases
- **One assertion per test** when possible — split multi-assertion tests into separate tests
- **Prefer factory functions** over complex fixtures when setup needs variation per test
- **Use parametrize** for testing multiple inputs with the same logic:

```python
@pytest.mark.parametrize("input_name, expected", [
    ("First Name", "first_name"),
    ("UPPER CASE", "upper_case"),
    ("already_clean", "already_clean"),
    ("  spaces  ", "spaces"),
])
def test_sanitize_column_name(input_name, expected):
    assert _sanitize_column_name(input_name) == expected
```

## Mocking Strategy

This project has several external dependency layers. Use the right mocking approach for each.

### Environment Variables

Use `monkeypatch` (preferred) or `pytest-mock`:

```python
def test_get_headers_with_valid_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    monkeypatch.setenv("API_URL", "https://api.example.com/v2")

    headers = _get_headers()

    assert headers["Authorization"] == "test-key-123"
```

```python
def test_get_headers_missing_key(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)

    with pytest.raises(ValueError, match="API_KEY"):
        _get_headers()
```

### HTTP Requests

Mock `requests.post` / `requests.get` — never make real HTTP calls in tests:

```python
def test_execute_graphql_query_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"me": {"id": "123"}}}
    mock_response.raise_for_status = mocker.Mock()

    mocker.patch("requests.post", return_value=mock_response)

    result = _execute_graphql_query("{ me { id } }")

    assert result["data"]["me"]["id"] == "123"
```

### SQLite / Database

Use in-memory SQLite databases via fixtures — no mocking needed:

```python
@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Provide an isolated in-memory-like test database."""
    db_path = tmp_path / "test.db"
    monkeypatch.setattr("mypackage.db.DB_PATH", str(db_path))
    init_db()
    return db_path
```

### File System

Use pytest's built-in `tmp_path` fixture for file operations:

```python
def test_list_downloaded_files(tmp_path, monkeypatch):
    monkeypatch.setattr("mypackage.downloader.RAW_DIR", str(tmp_path))
    (tmp_path / "data_2026.zip").touch()
    (tmp_path / "data_2025.zip").touch()

    result = list_downloaded_files()

    assert len(result) == 2
```

### Streamlit Caching Decorators

Disable Streamlit caching in tests by patching decorators to be pass-throughs:

```python
# In tests/conftest.py
@pytest.fixture(autouse=True)
def disable_streamlit_cache(monkeypatch):
    """Disable Streamlit caching decorators in tests."""
    try:
        import streamlit  # noqa: F401
    except ImportError:
        return
    monkeypatch.setattr("streamlit.cache_data", lambda func=None, **kwargs: func if func else lambda f: f)
    monkeypatch.setattr("streamlit.cache_resource", lambda func=None, **kwargs: func if func else lambda f: f)
```

### Google Drive / External APIs

Mock at the service-building boundary:

```python
def test_upload_file_to_gdrive(mocker, tmp_path):
    mock_service = mocker.Mock()
    mock_service.files.return_value.list.return_value.execute.return_value = {"files": []}
    mock_service.files.return_value.create.return_value.execute.return_value = {"id": "abc123"}
    mocker.patch("mypackage.gdrive._build_drive_service", return_value=mock_service)

    test_file = tmp_path / "test.csv"
    test_file.write_text("a,b\n1,2")

    result = upload_file_to_gdrive(str(test_file), "folder-id")

    assert result == "abc123"
```

## Quality Checklist

Apply this checklist to every test file before considering it complete:

- [ ] **Every public function has at least one test**
- [ ] **Happy path tested** — normal inputs produce expected outputs
- [ ] **Edge cases tested** — empty inputs, None values, boundary values
- [ ] **Error paths tested** — expected exceptions are raised with correct messages
- [ ] **No real external calls** — HTTP, database (unless in-memory), file I/O use mocks or tmp_path
- [ ] **Tests are independent** — no test depends on another test's state or execution order
- [ ] **Tests are deterministic** — no random failures, time-dependent logic is mocked
- [ ] **Descriptive names** — test name explains what is being tested and the scenario
- [ ] **Minimal fixtures** — fixtures provide only what's needed, not large shared state
- [ ] **Parametrize used** — when 3+ tests differ only by input/output, use `@pytest.mark.parametrize`

## What NOT to Test

- Streamlit UI rendering (st.title, st.markdown, st.button) — these are framework internals
- Third-party library internals (pandas DataFrame methods, requests library)
- Private functions that are only called through public interfaces (test via the public function)
- Constants and configuration values

## Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing

# Run a specific test file
uv run pytest tests/test_users.py -v

# Run a specific test
uv run pytest tests/test_users.py::TestGetHeaders::test_missing_api_key -v
```

## Procedure

1. **Read the source module** to understand all functions, their signatures, return types, and dependencies
2. **Identify what to mock** — list all external dependencies (env vars, HTTP, file system, databases)
3. **Create/update conftest.py** with shared fixtures if needed (see [conftest template](./assets/conftest_template.py))
4. **Write the test file** following the file template and project conventions
5. **Apply quality checklist** — verify all items pass
6. **Run tests** with `uv run pytest tests/<test_file>.py -v` and fix any failures
7. **Check coverage** with `uv run pytest tests/<test_file>.py --cov=src --cov-report=term-missing`
