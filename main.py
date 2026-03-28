"""FastAPI application for LLM evaluation webapp."""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
import uuid
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
logger.info("Starting LLM Evaluation System")

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Environment variables loaded from .env")
except ImportError:
    logger.warning("python-dotenv not available")

from lib.test_generator import generate_test_cases, validate_test_cases
from lib.llm_evaluator import LLMEvaluator

app = FastAPI(title="LLM Evaluation System")

# Store evaluation results in memory (in production, use a database)
evaluation_results = {}

# Serve static files
if not os.path.exists("static"):
    os.makedirs("static")

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    pass


class EvaluationRequest(BaseModel):
    """Request model for evaluation."""
    goal: str
    system_prompt: str
    num_test_cases: int = 10
    model: str = "llama-3.3-70b-versatile"
    provider: str = "groq"  # groq, openai, or anthropic
    api_key: Optional[str] = None  # Optional API key override
    test_cases: Optional[List[Dict[str, str]]] = None


class EvaluationResponse(BaseModel):
    """Response model for evaluation results."""
    evaluation_id: str
    status: str
    average_grade: float
    total_cases: int
    results: List[Dict[str, Any]]
    goal: str
    system_prompt: str
    created_at: str


@app.get("/")
async def root():
    """Serve the main HTML page."""
    return FileResponse("static/index.html", media_type="text/html")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "LLM Evaluation System is running"
    }


@app.post("/api/evaluate")
async def evaluate(request: EvaluationRequest, background_tasks: BackgroundTasks):
    """
    Start an evaluation.
    
    Args:
        request: Evaluation request with goal, system_prompt, and optionally test_cases
    
    Returns:
        Evaluation ID and initial response
    """
    try:
        logger.info(f"Received evaluation request for goal: {request.goal[:50]}...")
        logger.info(f"Provider: {request.provider}, Model: {request.model}")
        
        # Validate API key for the selected provider
        env_var_map = {
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY"
        }
        env_var = env_var_map.get(request.provider)
        
        api_key = request.api_key or os.getenv(env_var)
        if not api_key:
            logger.error(f"{env_var} not set and API key not provided in request")
            raise HTTPException(
                status_code=400,
                detail=f"{env_var} environment variable not set. Please provide API key in request or set environment variable."
            )
        
        # Generate or validate test cases
        if request.test_cases:
            logger.info(f"Using {len(request.test_cases)} custom test cases")
            if not validate_test_cases(request.test_cases):
                logger.error("Invalid test case format")
                raise HTTPException(
                    status_code=400,
                    detail="Invalid test case format. Each case must be a dict with 'task' key."
                )
            test_cases = request.test_cases
        else:
            logger.info(f"Generating {request.num_test_cases} test cases")
            test_cases = generate_test_cases(request.goal, request.num_test_cases)
            logger.info(f"Generated {len(test_cases)} test cases")
        
        # Create evaluation ID
        eval_id = str(uuid.uuid4())
        logger.info(f"Created evaluation ID: {eval_id}")
        
        # Initialize evaluator with provider
        logger.info(f"Initializing evaluator with provider: {request.provider}, model: {request.model}")
        evaluator = LLMEvaluator(
            api_key=api_key,
            model=request.model,
            provider=request.provider
        )
        
        # Run evaluation
        try:
            logger.info(f"Starting evaluation {eval_id}")
            result = evaluator.evaluate_all(
                test_cases=test_cases,
                system_prompt=request.system_prompt,
                goal=request.goal
            )
            
            # Store result
            evaluation_results[eval_id] = {
                **result,
                "created_at": datetime.now().isoformat(),
                "status": "completed"
            }
            logger.info(f"Evaluation {eval_id} completed. Average grade: {result['average_grade']}")
            
            response_data = {
                "evaluation_id": eval_id,
                "status": "completed",
                "average_grade": result["average_grade"],
                "total_cases": result["total_cases"],
                "results": result["results"],
                "goal": result["goal"],
                "system_prompt": result["system_prompt"],
                "created_at": evaluation_results[eval_id]["created_at"]
            }
            logger.info(f"Returning response with average_grade: {response_data['average_grade']}")
            logger.debug(f"Full result object - Total cases: {response_data['total_cases']}, Results count: {len(response_data['results'])}")
            return response_data
        
        except Exception as e:
            logger.error(f"Evaluation {eval_id} failed: {str(e)}", exc_info=True)
            evaluation_results[eval_id] = {
                "status": "error",
                "error": str(e),
                "created_at": datetime.now().isoformat()
            }
            raise HTTPException(
                status_code=500,
                detail=f"Evaluation failed: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.get("/api/evaluation/{eval_id}")
async def get_evaluation(eval_id: str):
    """
    Get evaluation results by ID.
    
    Args:
        eval_id: The evaluation ID
    
    Returns:
        Evaluation results
    """
    if eval_id not in evaluation_results:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation_results[eval_id]


@app.get("/api/evaluations")
async def list_evaluations():
    """List all evaluation results."""
    return {
        "count": len(evaluation_results),
        "evaluations": [
            {
                "id": eval_id,
                "status": data.get("status"),
                "average_grade": data.get("average_grade"),
                "created_at": data.get("created_at"),
                "goal": data.get("goal", "N/A")
            }
            for eval_id, data in evaluation_results.items()
        ]
    }


@app.post("/api/generate-test-cases")
async def generate_cases(goal: str, num_cases: int = 10):
    """
    Generate test cases based on a goal.
    
    Args:
        goal: The evaluation goal
        num_cases: Number of test cases to generate
    
    Returns:
        List of test cases
    """
    try:
        test_cases = generate_test_cases(goal, num_cases)
        return {
            "test_cases": test_cases,
            "count": len(test_cases)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
