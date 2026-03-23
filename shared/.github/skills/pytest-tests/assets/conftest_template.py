"""Shared pytest fixtures for the test suite."""

import sqlite3

import pytest


@pytest.fixture(autouse=True)
def disable_streamlit_cache(monkeypatch):
    """Disable Streamlit caching decorators so they don't interfere with tests."""
    try:
        import streamlit  # noqa: F401
    except ImportError:
        return
    monkeypatch.setattr(
        "streamlit.cache_data",
        lambda func=None, **kwargs: func if func else lambda f: f,
    )
    monkeypatch.setattr(
        "streamlit.cache_resource",
        lambda func=None, **kwargs: func if func else lambda f: f,
    )


@pytest.fixture
def in_memory_db():
    """Provide an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


@pytest.fixture
def mock_env(monkeypatch):
    """Provide a helper to set environment variables for tests.

    Usage:
        def test_something(mock_env):
            mock_env(MONDAY_API_KEY="test-key", MONDAY_API_URL="https://api.monday.com/v2")
    """

    def _set_env(**env_vars: str):
        for key, value in env_vars.items():
            monkeypatch.setenv(key, value)

    return _set_env


@pytest.fixture
def clear_env(monkeypatch):
    """Provide a helper to remove environment variables for tests.

    Usage:
        def test_missing_key(clear_env):
            clear_env("MONDAY_API_KEY", "MONDAY_API_URL")
    """

    def _clear_env(*env_vars: str):
        for key in env_vars:
            monkeypatch.delenv(key, raising=False)

    return _clear_env
