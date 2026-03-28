"""LLM Evaluation Library - Test generation and grading utilities."""

# Import only test_generator to avoid circular dependencies
try:
    from lib.test_generator import generate_test_cases, validate_test_cases
    __all__ = ['generate_test_cases', 'validate_test_cases']
except ImportError:
    __all__ = []

# LLMEvaluator can be imported separately when needed
# from lib.llm_evaluator import LLMEvaluator
