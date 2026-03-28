"""Generate test case datasets for LLM evaluation."""

import json
import random
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def generate_test_cases(goal: str, num_cases: int = 10) -> List[Dict[str, str]]:
    """
    Generate test cases based on the goal with specific distribution:
    - 25% positive cases (straightforward, clear questions)
    - 40% negative cases (tricky, ambiguous questions)
    - 25% extreme edge cases (boundary conditions, unusual inputs)
    - 10% non-related cases (off-topic questions)
    
    Args:
        goal: The evaluation goal describing what to test
        num_cases: Number of test cases to generate (default: 10)
    
    Returns:
        List of test case dictionaries with 'task' key
    """
    
    # Positive cases (25%) - Straightforward, clear questions
    positive_cases = [
        {"task": "What is 2+2?"},
        {"task": "What is the capital of France?"},
        {"task": "What is the smallest planet?"},
        {"task": "Define artificial intelligence."},
        {"task": "How do you boil water?"},
        {"task": "What is the purpose of a dictionary?"},
        {"task": "What is the largest ocean?"},
        {"task": "Who wrote Romeo and Juliet?"},
        {"task": "What is the color of the sky on a clear day?"},
        {"task": "How many continents are there?"},
    ]
    
    # Negative cases (40%) - Tricky, ambiguous, or challenging questions
    negative_cases = [
        {"task": "Explain the paradox of choice and its implications."},
        {"task": "What makes a question 'good'?"},
        {"task": "Discuss the ethics of artificial intelligence."},
        {"task": "How do you define success in an ambiguous context?"},
        {"task": "What is the difference between correlation and causation?"},
        {"task": "Explain why some people fear innovation."},
        {"task": "What are the limitations of machine learning?"},
        {"task": "How do you measure intelligence?"},
        {"task": "Describe the impact of bias in data."},
        {"task": "What makes a good explanation?"},
        {"task": "Explain the Dunning-Kruger effect."},
        {"task": "How does context affect meaning?"},
        {"task": "What are the trade-offs between simplicity and accuracy?"},
        {"task": "Discuss the nature of consciousness."},
        {"task": "What makes communication effective?"},
    ]
    
    # Extreme edge cases (25%) - Boundary conditions, unusual inputs
    extreme_cases = [
        {"task": "What is nothing?"},
        {"task": "Explain 0 divided by 0."},
        {"task": "What happens at the edge of a black hole?"},
        {"task": "Define the color that doesn't exist."},
        {"task": "How do you describe a sound to a deaf person?"},
        {"task": "What is the meaning of a word that has no definition?"},
        {"task": "Explain infinity to a child."},
        {"task": "What is the opposite of opposite?"},
        {"task": "How do you count to a number that doesn't exist?"},
        {"task": "Describe a taste that has no name."},
    ]
    
    # Non-related cases (10%) - Off-topic, unrelated questions
    non_related_cases = [
        {"task": "What is your favorite pizza topping?"},
        {"task": "Do you prefer cats or dogs?"},
        {"task": "What is the best movie of all time?"},
        {"task": "Should pineapple be on pizza?"},
        {"task": "What is the perfect temperature for coffee?"},
    ]
    
    # Calculate number of cases for each category
    num_positive = round(num_cases * 0.25)
    num_negative = round(num_cases * 0.40)
    num_extreme = round(num_cases * 0.25)
    num_non_related = round(num_cases * 0.10)
    
    logger.debug(f"Test case distribution - Positive: {num_positive}, Negative: {num_negative}, Extreme: {num_extreme}, Non-related: {num_non_related}")
    
    # Adjust if rounding causes total to not equal num_cases
    total = num_positive + num_negative + num_extreme + num_non_related
    if total > num_cases:
        # Reduce from the largest category (negative)
        num_negative -= (total - num_cases)
    elif total < num_cases:
        # Add to the largest category (negative)
        num_negative += (num_cases - total)
    
    # Ensure all counts are non-negative and don't exceed population
    num_positive = max(0, min(num_positive, len(positive_cases)))
    num_negative = max(0, min(num_negative, len(negative_cases)))
    num_extreme = max(0, min(num_extreme, len(extreme_cases)))
    num_non_related = max(0, min(num_non_related, len(non_related_cases)))
    
    # Select random cases from each category (only if count > 0)
    selected_positive = random.sample(positive_cases, num_positive) if num_positive > 0 else []
    selected_negative = random.sample(negative_cases, num_negative) if num_negative > 0 else []
    selected_extreme = random.sample(extreme_cases, num_extreme) if num_extreme > 0 else []
    selected_non_related = random.sample(non_related_cases, num_non_related) if num_non_related > 0 else []
    
    # Combine all cases
    test_cases = selected_positive + selected_negative + selected_extreme + selected_non_related
    
    # Shuffle to mix the distribution
    random.shuffle(test_cases)
    
    logger.info(f"Generated {len(test_cases[:num_cases])} test cases for goal: {goal[:50]}...")
    return test_cases[:num_cases]


def validate_test_cases(test_cases: List[Dict[str, Any]]) -> bool:
    """
    Validate that test cases have the correct format.
    
    Args:
        test_cases: List of test case dictionaries
    
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(test_cases, list):
        return False
    
    for case in test_cases:
        if not isinstance(case, dict) or "task" not in case:
            return False
    
    return True
