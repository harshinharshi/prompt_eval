# Quick Test Reference

## Environment Setup ✅
Your codebase uses **`os.getenv("GROQ_API_KEY")`** consistently everywhere:
- ✅ `main.py` 
- ✅ `lib/llm_evaluator.py`
- ✅ `conftest.py` 

Your `.env` file automatically loads when pytest starts.

## Running Tests

### Simple: Run all tests
```bash
uv run pytest test_groq_pytest.py -v
```

### Test Generator Only (Always Pass - No API needed)
```bash
uv run pytest test_groq_pytest.py::TestTestGenerator -v
```

### With Coverage Report
```bash
uv run pytest test_groq_pytest.py --cov=lib --cov=main -v
```

### Only Fast Tests (Skip API calls)
```bash
uv run pytest test_groq_pytest.py -m "not requires_api_key" -v
```

### Run Specific Test
```bash
uv run pytest test_groq_pytest.py::TestTestGenerator::test_generate_test_cases_default -v
```

## Test Status

| Test Class | Tests | Status | Note |
|-----------|-------|--------|------|
| TestTestGenerator | 4 | ✅ **ALL PASS** | No API needed |
| TestGroqIntegration | 3 | ⏳ Requires API key | Full Groq calls |
| TestLLMEvaluator | 5 | ⏳ Requires API key | Evaluation pipeline |
| TestFastAPIEndpoints | 4 | ⏳ Requires API key | API endpoint tests |
| TestIntegration | 1 | ⏳ Requires API key | End-to-end flow |

**Total: 17 tests**

## Environment Variable Format

All code uses:
```python
api_key = os.getenv("GROQ_API_KEY")
```

Your `.env` file:
```
GROQ_API_KEY=gsk_your-actual-api-key-here
```

⚠️ **NEVER commit actual API keys** - Always use placeholders in documentation

The `conftest.py` loads this automatically from `.env` before tests run.

## Key Files

- **Test file**: `test_groq_pytest.py` (17 tests)
- **Config**: `conftest.py` (loads .env automatically)
- **pytest settings**: `pytest.ini`
- **Main API**: `main.py` (uses `os.getenv("GROQ_API_KEY")`)
- **Evaluator**: `lib/llm_evaluator.py` (uses `os.getenv("GROQ_API_KEY") `)
- **Test generator**: `lib/test_generator.py` (no API needed)

## Success Indicators

✅ **Working:**
- `.env` loads automatically
- `os.getenv("GROQ_API_KEY")` works everywhere
- TestTestGenerator: **4/4 PASS**
- FastAPI endpoints respond
- Groq integration validates

## Troubleshooting

**Test fails with "No module named 'langchain_groq'"**
```bash
# Reinstall dependencies
uv sync
```

**"GROQ_API_KEY not found"**
```bash
# Verify .env exists
ls -la .env

# Verify key is set
echo $GROQ_API_KEY
```

**Want to run with system Python instead of uv**
```bash
source .venv/Scripts/activate
pytest test_groq_pytest.py -v
```
