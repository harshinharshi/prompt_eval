"""
Pytest test suite for LLM Evaluation System with multi-provider support.
Tests Groq, OpenAI, and Anthropic integration with LangChain.
Tests include test case generation, LLM evaluation, and API endpoints.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv optional for tests


class TestMultiProviderInitialization:
    """Test provider initialization with LangChain."""
    
    @pytest.mark.requires_api_key
    def test_groq_api_key_exists(self):
        """Test that GROQ_API_KEY is available in environment."""
        api_key = os.getenv("GROQ_API_KEY")
        assert api_key is not None, "GROQ_API_KEY not found in environment"
        assert api_key.startswith("gsk"), "Groq API key should start with 'gsk'"
    
    def test_openai_api_key_format(self):
        """Test OpenAI API key format if available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            assert api_key.startswith("sk-"), "OpenAI API key should start with 'sk-'"
    
    def test_anthropic_api_key_format(self):
        """Test Anthropic API key format if available."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            assert api_key.startswith("sk-ant-"), "Anthropic API key should start with 'sk-ant-'"
    
    @pytest.mark.requires_api_key
    def test_chatgroq_initialization(self):
        """Test that ChatGroq client can be initialized."""
        from langchain_groq import ChatGroq
        
        api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
        )
        assert llm is not None
        assert llm.model_name == "llama-3.3-70b-versatile"
    
    def test_chatopenai_initialization(self):
        """Test that ChatOpenAI client can be initialized if API key available."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0.7)
        assert llm is not None
    
    def test_chatanthropic_initialization(self):
        """Test that ChatAnthropic client can be initialized if API key available."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        from langchain_anthropic import ChatAnthropic
        llm = ChatAnthropic(api_key=api_key, model="claude-3-5-sonnet-20241022", temperature=0.7)
        assert llm is not None
    
    def test_simple_groq_message_response(self):
        """Test sending a simple message and receiving a response from Groq."""
        from langchain_groq import ChatGroq
        from langchain_core.messages import HumanMessage
        
        api_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
            groq_api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0.3,
        )
        
        messages = [HumanMessage(content="what is 2+2?")]
        response = llm.invoke(messages)
        
        assert response is not None
        assert response.content is not None
        assert len(response.content) > 0
        assert "4" in response.content.lower()


class TestTestGenerator:
    """Test the test case generation module."""
    
    def test_generate_test_cases_default(self):
        """Test generating default number of test cases."""
        from lib.test_generator import generate_test_cases
        
        test_cases = generate_test_cases(goal="test evaluation", num_cases=10)
        
        assert isinstance(test_cases, list)
        assert len(test_cases) == 10
        assert all("task" in case for case in test_cases)
        assert all(isinstance(case, dict) for case in test_cases)
    
    def test_generate_test_cases_custom_count(self):
        """Test generating custom number of test cases."""
        from lib.test_generator import generate_test_cases
        
        test_cases = generate_test_cases(goal="test evaluation", num_cases=5)
        assert len(test_cases) == 5
        
        test_cases = generate_test_cases(goal="test evaluation", num_cases=15)
        assert len(test_cases) == 15
    
    def test_validate_test_cases_valid(self):
        """Test validating correct test case format."""
        from lib.test_generator import validate_test_cases
        
        valid_cases = [
            {"task": "What is 2+2?"},
            {"task": "Define AI"},
        ]
        
        assert validate_test_cases(valid_cases) is True
    
    def test_validate_test_cases_invalid_format(self):
        """Test validating incorrect test case formats."""
        from lib.test_generator import validate_test_cases
        
        # Missing 'task' key
        invalid_cases_1 = [{"question": "What is 2+2?"}]
        assert validate_test_cases(invalid_cases_1) is False
        
        # Not a list
        invalid_cases_2 = {"task": "What is 2+2?"}
        assert validate_test_cases(invalid_cases_2) is False
        
        # Not dictionaries
        invalid_cases_3 = ["What is 2+2?"]
        assert validate_test_cases(invalid_cases_3) is False


class TestLLMEvaluator:
    """Test the LLM Evaluator class with multi-provider support."""
    
    def test_llm_evaluator_groq_initialization(self):
        """Test that LLMEvaluator can be initialized with Groq."""
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        evaluator = LLMEvaluator(
            api_key=api_key, 
            model="llama-3.3-70b-versatile",
            provider="groq"
        )
        
        assert evaluator is not None
        assert evaluator.provider == "groq"
        assert evaluator.model == "llama-3.3-70b-versatile"
    
    def test_llm_evaluator_openai_initialization(self):
        """Test that LLMEvaluator can be initialized with OpenAI."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        from lib.llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator(
            api_key=api_key,
            model="gpt-4o",
            provider="openai"
        )
        
        assert evaluator is not None
        assert evaluator.provider == "openai"
        assert evaluator.model == "gpt-4o"
    
    def test_llm_evaluator_anthropic_initialization(self):
        """Test that LLMEvaluator can be initialized with Anthropic."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        from lib.llm_evaluator import LLMEvaluator
        
        evaluator = LLMEvaluator(
            api_key=api_key,
            model="claude-3-5-sonnet-20241022",
            provider="anthropic"
        )
        
        assert evaluator is not None
        assert evaluator.provider == "anthropic"
        assert evaluator.model == "claude-3-5-sonnet-20241022"
    
    def test_llm_evaluator_default_provider(self):
        """Test that LLMEvaluator uses Groq as default provider."""
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        evaluator = LLMEvaluator(api_key=api_key)
        
        assert evaluator.provider == "groq"
        assert evaluator.model == "llama-3.3-70b-versatile"
    
    def test_llm_evaluator_missing_api_key(self):
        """Test that LLMEvaluator raises error when API key is missing."""
        from lib.llm_evaluator import LLMEvaluator
        
        with pytest.raises(ValueError, match="API_KEY not provided"):
            evaluator = LLMEvaluator(
                api_key=None,
                model="gpt-4o",
                provider="openai"
            )
    
    def test_generate_responses(self):
        """Test generating responses for test cases."""
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        evaluator = LLMEvaluator(api_key=api_key, model="llama-3.3-70b-versatile", provider="groq")
        
        test_cases = [
            {"task": "What is 2+2?"},
            {"task": "What is the capital of France?"},
        ]
        system_prompt = "You are a helpful assistant."
        
        results = evaluator.generate_responses(test_cases, system_prompt)
        
        assert isinstance(results, list)
        assert len(results) == 2
        assert all("response" in result for result in results)
        assert all("task" in result for result in results)
        assert all(isinstance(result["response"], str) for result in results)
    
    def test_grade_response(self):
        """Test grading a single response."""
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        evaluator = LLMEvaluator(
            api_key=api_key, 
            model="llama-3.3-70b-versatile",
            provider="groq"
        )
        
        task = "What is 2+2?"
        response = "The answer is 4."
        goal = "Evaluate mathematical accuracy"
        system_prompt = "You are a helpful assistant."
        
        grade, reasoning = evaluator.grade_response(
            task=task,
            response=response,
            goal=goal,
            system_prompt=system_prompt
        )
        
        assert isinstance(grade, int)
        assert 1 <= grade <= 10, "Grade should be between 1 and 10"
        assert isinstance(reasoning, str)
        assert len(reasoning) > 0
    
    def test_evaluate_all(self):
        """Test complete evaluation pipeline."""
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        evaluator = LLMEvaluator(
            api_key=api_key, 
            model="llama-3.3-70b-versatile",
            provider="groq"
        )
        
        test_cases = [
            {"task": "What is 2+2?"},
            {"task": "What is the largest planet?"},
        ]
        system_prompt = "You are a helpful assistant. Provide accurate answers."
        goal = "Evaluate accuracy and helpfulness"
        
        result = evaluator.evaluate_all(test_cases, system_prompt, goal)
        
        assert isinstance(result, dict)
        assert "results" in result
        assert "average_grade" in result
        assert "total_cases" in result
        assert result["total_cases"] == 2
        assert isinstance(result["average_grade"], float)
        assert 1 <= result["average_grade"] <= 10


class TestFastAPIEndpoints:
    """Test FastAPI endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the FastAPI app."""
        from fastapi.testclient import TestClient
        from main import app
        
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_generate_test_cases_endpoint(self, client):
        """Test the test case generation endpoint."""
        response = client.post("/api/generate-test-cases?goal=test&num_cases=5")
        
        assert response.status_code == 200
        data = response.json()
        assert "test_cases" in data
        assert "count" in data
        assert data["count"] == 5
        assert len(data["test_cases"]) == 5
    
    def test_evaluate_endpoint_missing_goal(self, client):
        """Test evaluate endpoint with missing goal."""
        response = client.post(
            "/api/evaluate",
            json={
                "system_prompt": "You are helpful"
            }
        )
        
        assert response.status_code == 422  # Validation error
    
    def test_evaluate_endpoint_missing_api_key(self, client):
        """Test evaluate endpoint when API key is not set."""
        with patch.dict(os.environ, {}, clear=False):
            # Temporarily remove all API keys
            for key in ["GROQ_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]:
                if key in os.environ:
                    del os.environ[key]
            
            # Make request without providing API key
            response = client.post(
                "/api/evaluate",
                json={
                    "goal": "Test evaluation",
                    "system_prompt": "You are helpful",
                    "num_test_cases": 2,
                    "provider": "groq"
                    # Note: api_key is optional in request
                }
            )
            
            assert response.status_code == 400
            data = response.json()
            assert "API" in data["detail"] or "key" in data["detail"].lower()
    
    def test_evaluate_endpoint_with_provider(self, client):
        """Test evaluate endpoint with different provider specified."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            pytest.skip("GROQ_API_KEY not set")
        
        response = client.post(
            "/api/evaluate",
            json={
                "goal": "Test evaluation",
                "system_prompt": "You are helpful",
                "num_test_cases": 2,
                "provider": "groq",
                "api_key": api_key
            }
        )
        
        # Should either succeed or fail due to rate limiting, not missing key
        assert response.status_code in [200, 429, 500]


class TestIntegration:
    """Integration tests for the complete system with multi-provider support."""
    
    def test_end_to_end_evaluation_groq(self):
        """Test the complete evaluation workflow with Groq."""
        from lib.test_generator import generate_test_cases
        from lib.llm_evaluator import LLMEvaluator
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            pytest.skip("GROQ_API_KEY not set")
        
        # Step 1: Generate test cases
        goal = "Evaluate mathematical reasoning"
        test_cases = generate_test_cases(goal, num_cases=2)
        assert len(test_cases) == 2
        
        # Step 2: Create evaluator with Groq
        evaluator = LLMEvaluator(api_key=api_key, provider="groq")
        assert evaluator is not None
        assert evaluator.provider == "groq"
        
        # Step 3: Run evaluation
        system_prompt = "You are a mathematical assistant. Provide step-by-step explanations."
        result = evaluator.evaluate_all(test_cases, system_prompt, goal)
        
        # Step 4: Verify results
        assert "results" in result
        assert "average_grade" in result
        assert len(result["results"]) == 2
        assert 1 <= result["average_grade"] <= 10
        
        # Verify each result has required fields
        for res in result["results"]:
            assert "task" in res
            assert "response" in res
            assert "grade" in res
            assert "reasoning" in res
    
    def test_end_to_end_evaluation_openai(self):
        """Test the complete evaluation workflow with OpenAI."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            pytest.skip("OPENAI_API_KEY not set")
        
        from lib.test_generator import generate_test_cases
        from lib.llm_evaluator import LLMEvaluator
        
        # Step 1: Generate test cases
        goal = "Evaluate mathematical reasoning"
        test_cases = generate_test_cases(goal, num_cases=2)
        assert len(test_cases) == 2
        
        # Step 2: Create evaluator with OpenAI
        evaluator = LLMEvaluator(api_key=api_key, provider="openai", model="gpt-4o")
        assert evaluator is not None
        assert evaluator.provider == "openai"
        
        # Step 3: Run evaluation
        system_prompt = "You are a helpful assistant."
        result = evaluator.evaluate_all(test_cases, system_prompt, goal)
        
        # Step 4: Verify results
        assert "results" in result
        assert "average_grade" in result
        assert len(result["results"]) == 2
        assert 1 <= result["average_grade"] <= 10
    
    def test_end_to_end_evaluation_anthropic(self):
        """Test the complete evaluation workflow with Anthropic."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            pytest.skip("ANTHROPIC_API_KEY not set")
        
        from lib.test_generator import generate_test_cases
        from lib.llm_evaluator import LLMEvaluator
        
        # Step 1: Generate test cases
        goal = "Evaluate mathematical reasoning"
        test_cases = generate_test_cases(goal, num_cases=2)
        assert len(test_cases) == 2
        
        # Step 2: Create evaluator with Anthropic
        evaluator = LLMEvaluator(
            api_key=api_key, 
            provider="anthropic", 
            model="claude-3-5-sonnet-20241022"
        )
        assert evaluator is not None
        assert evaluator.provider == "anthropic"
        
        # Step 3: Run evaluation
        system_prompt = "You are a helpful assistant."
        result = evaluator.evaluate_all(test_cases, system_prompt, goal)
        
        # Step 4: Verify results
        assert "results" in result
        assert "average_grade" in result
        assert len(result["results"]) == 2
        assert 1 <= result["average_grade"] <= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
