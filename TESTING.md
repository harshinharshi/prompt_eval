# Testing Guide

## Overview

This project includes comprehensive pytest test suite for testing the Groq LangChain integration, test case generation, LLM evaluation, and API endpoints.

## Test Files

- `test_groq_pytest.py` - Main test suite with unit and integration tests
- `conftest.py` - Pytest configuration and shared fixtures
- `pytest.ini` - Pytest configuration file

## Running Tests

### Install testing dependencies

```bash
# Using uv
uv sync --extra dev

# Or using pip
pip install -r requirements.txt
```

### Run all tests

```bash
pytest
```

### Run tests with verbose output

```bash
pytest -v
```

### Run with coverage report

```bash
pytest --cov=lib --cov=main --cov-report=html
```

### Run specific test class

```bash
pytest test_groq_pytest.py::TestGroqIntegration -v
```

### Run specific test

```bash
pytest test_groq_pytest.py::TestGroqIntegration::test_chatgroq_initialization -v
```

### Run only fast tests (skip slow ones)

```bash
pytest -m "not slow" -v
```

### Run only API tests

```bash
pytest -m "api" -v
```

## Test Structure

### TestGroqIntegration
Tests the basic Groq + LangChain integration:
- API key availability
- ChatGroq client initialization
- Simple message invocation and response

### TestTestGenerator
Tests the test case generation module:
- Default test case generation
- Custom count test case generation
- Test case validation (valid and invalid formats)

### TestLLMEvaluator
Tests the LLMEvaluator class:
- Initialization with custom parameters
- Default model selection
- Response generation for test cases
- Single response grading
- Complete evaluation pipeline

### TestFastAPIEndpoints
Tests API endpoints:
- Health check endpoint
- Test case generation endpoint
- Evaluate endpoint validation
- API key requirement validation

### TestIntegration
End-to-end integration tests:
- Complete evaluation workflow

## Environment Setup

Ensure your `.env` file has:
```bash
GROQ_API_KEY=gsk-your-api-key-here
```

## Test Markers

Available pytest markers:
- `@pytest.mark.slow` - Slower tests
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.api` - API endpoint tests
- `@pytest.mark.groq` - Tests requiring Groq API

Example usage:
```bash
pytest -m "groq" -v
```

## Coverage Reports

Generate and view coverage:

```bash
# Generate coverage report
pytest --cov=lib --cov=main --cov-report=html

# Open in browser (on Windows)
start htmlcov/index.html

# On Linux/Mac
open htmlcov/index.html
```

## Expected Test Results

When all tests pass, you should see:
- ✓ Groq integration tests (API key, client init, message response)
- ✓ Test generator tests (generation, validation)
- ✓ LLM Evaluator tests (init, responses, grading, evaluation)
- ✓ FastAPI endpoint tests (health, generate, evaluate)
- ✓ Integration tests (end-to-end workflow)

Total: Typically 15+ test cases

## Troubleshooting

### "GROQ_API_KEY not found"
- Ensure `.env` file exists with valid API key
- Run `export GROQ_API_KEY=gsk-...` in terminal

### "Test hangs or times out"
- Some tests make actual Groq API calls (0.5-2 minutes for full suite)
- Use `pytest -m "not slow"` to skip slow tests
- Check your internet connection and API rate limits

### "ModuleNotFoundError"
- Ensure all dependencies installed: `uv sync` or `pip install -r requirements.txt`
- Ensure you're in the virtual environment

## Performance Notes

- Unit tests: Fast (< 1 second each)
- Integration tests: Slow (requires Groq API calls, 30-60 seconds total)
- Full test suite: ~2-3 minutes

## CI/CD Integration

Example GitHub Actions workflow (optional):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - run: pip install -r requirements.txt
      - run: pytest --cov=lib --cov=main
```
