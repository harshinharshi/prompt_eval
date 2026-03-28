"""LLM evaluation and grading system with support for multiple providers."""

import json
import logging
from typing import List, Dict, Any, Tuple
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import os

logger = logging.getLogger(__name__)


class LLMEvaluator:
    """Evaluate LLM responses using system prompts and grading criteria."""
    
    def __init__(
        self, 
        api_key: str = None, 
        model: str = "llama-3.3-70b-versatile",
        provider: str = "groq"
    ):
        """
        Initialize the evaluator with multi-provider LLM support.
        
        Args:
            api_key: API key for the provider (overrides env vars)
            model: Model name 
            provider: LLM provider - "groq", "openai", or "anthropic"
        """
        self.provider = provider
        self.model = model
        self.api_key = api_key
        
        logger.info(f"Initializing LLMEvaluator with provider: {provider}, model: {model}")
        
        # Initialize LLM based on provider
        self.llm = self._create_llm_instance(temperature=0.7)
        self.grader = self._create_llm_instance(temperature=0.3)
        
        logger.info("LLMEvaluator initialized successfully")
    
    def _create_llm_instance(self, temperature: float = 0.7):
        """Create LLM instance based on provider."""
        if self.provider == "groq":
            api_key = self.api_key or os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not provided")
            logger.debug(f"Creating ChatGroq instance")
            return ChatGroq(
                groq_api_key=api_key,
                model=self.model,
                temperature=temperature
            )
        
        elif self.provider == "openai":
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not provided")
            logger.debug(f"Creating ChatOpenAI instance")
            return ChatOpenAI(
                api_key=api_key,
                model=self.model,
                temperature=temperature
            )
        
        elif self.provider == "anthropic":
            api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not provided")
            logger.debug(f"Creating ChatAnthropic instance")
            return ChatAnthropic(
                api_key=api_key,
                model=self.model,
                temperature=temperature
            )
        
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    def generate_responses(
        self, 
        test_cases: List[Dict[str, str]], 
        system_prompt: str
    ) -> List[Dict[str, Any]]:
        """
        Generate LLM responses for each test case.
        
        Args:
            test_cases: List of test case dicts with 'task' key
            system_prompt: System instruction for the LLM
        
        Returns:
            List of test cases with added 'response' key
        """
        results = []
        logger.info(f"Generating responses for {len(test_cases)} test cases")
        
        for idx, test_case in enumerate(test_cases, 1):
            task = test_case.get("task", "")
            
            try:
                logger.debug(f"Processing test case {idx}/{len(test_cases)}: {task[:50]}...")
                # Create messages for the LLM
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=task)
                ]
                
                # Get response
                response = self.llm.invoke(messages)
                response_text = response.content
                logger.debug(f"Received response for test case {idx}")
                
                # Add response to result
                result = {**test_case, "response": response_text}
                results.append(result)
            except Exception as e:
                logger.error(f"Error generating response for test case {idx}: {str(e)}", exc_info=True)
                # Handle errors gracefully
                result = {
                    **test_case,
                    "response": f"Error: {str(e)}",
                    "error": True
                }
                results.append(result)
        
        return results
    
    def grade_response(
        self,
        task: str,
        response: str,
        goal: str,
        system_prompt: str
    ) -> Tuple[int, str]:
        """
        Grade a single response using the grading LLM.
        
        Args:
            task: The original task/question
            response: The LLM's response
            goal: The evaluation goal
            system_prompt: The system prompt that was used
        
        Returns:
            Tuple of (grade: int, reasoning: str)
        """
        grading_prompt = f"""You are an expert evaluator. Grade the following response based on the evaluation goal and system prompt provided.

Goal: {goal}

System Prompt: {system_prompt}

Task/Question: {task}

Response: {response}

Provide your evaluation in the following JSON format:
{{
    "grade": <number between 1 and 10>,
    "reasoning": "<explanation of the grade>"
}}

Respond ONLY with valid JSON, no additional text."""
        
        try:
            messages = [
                HumanMessage(content=grading_prompt)
            ]
            
            response_msg = self.grader.invoke(messages)
            response_text = response_msg.content
            
            # Parse JSON response
            # Try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                grade = int(result.get("grade", 5))
                reasoning = result.get("reasoning", "No reasoning provided")
                logger.debug(f"Grading result: grade={grade}")
            else:
                grade = 5
                reasoning = "Could not parse grading response"
                logger.warning(f"Could not parse grading response for task: {task[:50]}...")
            
            # Ensure grade is between 1 and 10
            grade = max(1, min(10, grade))
            
            return grade, reasoning
        except Exception as e:
            return 5, f"Grading error: {str(e)}"
    
    def evaluate_all(
        self,
        test_cases: List[Dict[str, str]],
        system_prompt: str,
        goal: str
    ) -> Dict[str, Any]:
        """
        Complete evaluation pipeline: generate responses and grade them.
        
        Args:
            test_cases: List of test case dicts with 'task' key
            system_prompt: System instruction for the response LLM
            goal: Evaluation goal for the grading LLM
        
        Returns:
            Dictionary with results, grades, and statistics
        """
        # Generate responses
        responses_data = self.generate_responses(test_cases, system_prompt)
        
        # Grade each response
        graded_results = []
        grades = []
        
        logger.info(f"Starting grading for {len(responses_data)} responses")
        for idx, item in enumerate(responses_data, 1):
            task = item.get("task", "")
            response = item.get("response", "")
            logger.debug(f"Grading response {idx}/{len(responses_data)}")
            
            grade, reasoning = self.grade_response(
                task=task,
                response=response,
                goal=goal,
                system_prompt=system_prompt
            )
            
            grades.append(grade)
            graded_results.append({
                "task": task,
                "response": response,
                "grade": grade,
                "reasoning": reasoning
            })
        
        # Calculate statistics
        avg_grade = sum(grades) / len(grades) if grades else 0
        logger.info(f"Individual grades collected: {grades}")
        logger.info(f"Total grades count: {len(grades)}")
        logger.info(f"Sum of grades: {sum(grades)}")
        logger.info(f"Calculated average grade: {avg_grade:.2f}")
        
        return {
            "results": graded_results,
            "average_grade": round(avg_grade, 2),
            "total_cases": len(graded_results),
            "goal": goal,
            "system_prompt": system_prompt
        }
