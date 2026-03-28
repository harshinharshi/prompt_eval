# LLM Evaluation System

A comprehensive web application for evaluating LLM responses with automated grading using **Groq** for fast and cost-effective inference.

## Features

✨ **Key Capabilities:**
- Input custom evaluation goals and system prompts
- Auto-generate test cases or provide your own in JSON format  
- Feed test cases to a Groq LLM with your system prompt
- Automatically grade responses using a grading LLM (1-10 scale)
- Get detailed reasoning for each grade
- View average scores and comprehensive results
- Download results as JSON
- **Fast inference with Groq** - 10x faster than traditional LLMs

## Architecture

The system works in 4 stages:

1. **Test Case Generation** - Creates at least 10 diverse test cases
2. **Response Generation** - LLM responds to each test case using your system prompt
3. **Response Storage** - Responses stored with original task
4. **Automated Grading** - Grading LLM evaluates each response and provides grades (1-10) with reasoning
5. **Results Display** - Shows average grade, all responses, grades, and reasoning

## Setup

### Prerequisites

- Python 3.13+ (or check your `.python-version` file)
- Groq API key (free tier available at https://console.groq.com)
- uv (UV package manager) - recommended

### Installation

1. **Install dependencies:**

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

2. **Set up environment variables (Optional - you can also provide keys in the UI):**

```bash
# For Groq (free, recommended)
export GROQ_API_KEY="gsk-your-api-key-here"

# For OpenAI (optional)
export OPENAI_API_KEY="sk-your-api-key-here"

# For Anthropic Claude (optional)
export ANTHROPIC_API_KEY="sk-ant-your-api-key-here"
```

On Windows:
```cmd
set GROQ_API_KEY=gsk-your-api-key-here
set OPENAI_API_KEY=sk-your-api-key-here
set ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

## Quick Start

**Run the application:**

```bash
uv run main.py
```

The web interface will be available at: **http://localhost:8000**

## Features

### Multi-Provider LLM Support

Choose from three powerful LLM providers:

1. **Groq** (Free & Fast)
   - Free tier available
   - 10x faster than traditional LLMs
   - Get key: https://console.groq.com

2. **OpenAI (GPT)**
   - Latest: GPT-5.4 series (5.4 Pro, 5.4 Thinking, 5.4 Mini, 5.4 Nano)
   - Also available: GPT-5.2, GPT-4o, GPT-4 Turbo
   - Requires paid API key
   - Get key: https://platform.openai.com/api-keys

3. **Anthropic (Claude)**
   - Latest: Claude 4.x series (Opus 4.6, Sonnet 4.6, Haiku 4.5)
   - Also available: Claude Opus 4.5, Claude Sonnet 4.5, Claude 3.5 Sonnet
   - Requires paid API key  
   - Get key: https://console.anthropic.com

**In the UI:** Select your provider, optionally enter an API key, and pick your model!

### Running the Application

```bash
# With uv
uv run main.py

# Or with Python directly
python main.py
```

The web interface will be available at: **http://localhost:8000**

## Usage

1. **Fill in the Evaluation Setup:**
   - Enter your **Evaluation Goal** (what you want to evaluate)
   - Enter your **System Prompt** (instructions for the LLM)
   - Optionally customize the number of test cases
   - Optionally provide custom test cases as JSON

2. **Start Evaluation:**
   - Click "Start Evaluation"
   - System will generate test cases, get responses, and grade them
   - This typically takes 1-3 minutes depending on test case count

3. **View Results:**
   - See average grade and statistics
   - Browse individual test cases with grades and reasoning
   - View the goal and system prompt used
   - Download results as JSON

## API Endpoints

### POST /api/evaluate
Start a new evaluation

**Request body:**
```json
{
  "goal": "Evaluate accuracy of answers",
  "system_prompt": "You are helpful assistant",
  "num_test_cases": 10,
  "model": "gpt-4",
  "test_cases": null
}
```

**Response:**
```json
{
  "evaluation_id": "uuid",
  "status": "completed",
  "average_grade": 8.5,
  "total_cases": 10,
  "results": [...],
  "goal": "...",
  "system_prompt": "...",
  "created_at": "2024-..."
}
```

### GET /api/evaluation/{eval_id}
Get results of a specific evaluation

### GET /api/evaluations
List all evaluations

### POST /api/generate-test-cases
Generate test cases for a goal

```
?goal=Evaluate+accuracy&num_cases=10
```

## Project Structure

```
prompt_eval/
├── main.py                 # FastAPI application and routes
├── lib/
│   ├── test_generator.py   # Test case generation logic
│   └── llm_evaluator.py    # LLM calling and grading logic
├── static/
│   └── index.html          # Web UI (HTML/CSS/JavaScript)
├── pyproject.toml          # Project configuration
├── .env                    # Environment variables (create this)
└── README.md              # This file
```

## Example Evaluation

**Goal:** "Evaluate the assistant's ability to provide clear, accurate, and helpful answers"

**System Prompt:** "You are a helpful, accurate, and clear assistant. Provide concise but informative answers."

**Test Cases:** Auto-generated (10 diverse questions)

**Output:** 
- Average grade: 8.2/10
- Individual grades for each response
- Reasoning for each grade
- Downloadable JSON results

## Configuration

### Models Available

**Groq Models** (Free & Fast)
- `llama-3.3-70b-versatile` - Llama 3.3 70B (default)
- `llama-3.1-70b-versatile` - Llama 3.1 70B
- `llama-3.1-8b-instant` - Llama 3.1 8B (fastest)
- `mixtral-8x7b-32768` - Mixtral 8x7B
- `openai/gpt-oss-120b` - GPT-OSS 120B
- `openai/gpt-oss-20b` - GPT-OSS 20B

**OpenAI Models** (Paid)
- `gpt-5-4` - **GPT-5.4 Flagship** (Latest, best overall)
- `gpt-5-4-pro` - GPT-5.4 Pro (Highest performance)
- `gpt-5-4-thinking` - GPT-5.4 Thinking (Deep reasoning)
- `gpt-5-4-mini` - GPT-5.4 Mini (Fast & economical)
- `gpt-5-4-nano` - GPT-5.4 Nano (Ultra-lightweight)
- `gpt-5-2` - GPT-5.2 (Production proven)
- `gpt-4o` - GPT-4o (Legacy)
- `gpt-4-turbo` - GPT-4 Turbo (Legacy)

**Anthropic Models** (Paid)
- `claude-opus-4-6` - **Claude Opus 4.6** (Most powerful, best reasoning)
- `claude-sonnet-4-6` - Claude Sonnet 4.6 (Balanced speed/intelligence)
- `claude-haiku-4-5` - Claude Haiku 4.5 (Fastest, most economical)
- `claude-opus-4-5` - Claude Opus 4.5 (Previous generation)
- `claude-sonnet-4-5` - Claude Sonnet 4.5 (Previous generation)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet (Legacy)

### Environment Variables
```bash
GROQ_API_KEY=gsk-...  # Your Groq API key (required)
```

## Development

To modify or extend the system:

1. **Add test case templates** in `lib/test_generator.py`
2. **Modify grading criteria** in `lib/llm_evaluator.py`
3. **Update UI** in `static/index.html`

## Testing

Run the comprehensive test suite:

```bash
uv run pytest test_groq_pytest.py -v
```

This runs 17+ tests covering:
- Test case generation with proper distribution (25% positive, 40% negative, 25% edge cases, 10% non-related)
- Groq API integration
- LLM evaluator functionality
- FastAPI endpoints
- End-to-end evaluation workflow

## Troubleshooting

**"GROQ_API_KEY environment variable not set"**
- Set your Groq API key: `export GROQ_API_KEY="gsk-..."`
- Get a free key at https://console.groq.com

**Evaluation takes forever**
- Groq is usually very fast, but check your API rate limits
- Try reducing number of test cases
- Use a faster model like `llama-3.1-8b-instant`

**Invalid test case format**
- Ensure JSON matches format: `[{"task": "question"}, ...]`

## Performance Notes

- Each evaluation typically takes **30 seconds - 2 minutes** (10 test cases)
- Groq is **10x faster than OpenAI** for similar quality
- Using `llama-3.1-8b-instant` is fastest
- Grade accuracy improves with clearer evaluation goals

## License

This project is open source.

## Support

For issues or questions, check the logs or ensure:
1. OpenAI API key is valid and has available credits
2. You have internet connectivity
3. The JSON format is correct for custom test cases
