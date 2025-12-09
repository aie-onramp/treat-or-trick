# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**TreatOrHell** is a FastAPI application providing an LLM-powered Angel persona that delivers emotional, sparkly CV/candidate feedback. This is an educational project for AI Engineer Onramp (AIE02) Session 2, demonstrating FastAPI backend development, OpenAI integration, and serverless deployment to Vercel.

**Core Features:**
- Angel chat endpoint with context-aware responses
- Student questionnaire for personalized feedback
- Dual storage strategy (file-based local, Redis on Vercel)
- Structured logging with token tracking and cost estimation
- Retry logic for OpenAI API calls

## Critical Architecture

### Vercel Deployment Entry Point
**CRITICAL:** The Vercel entry point is `api/index.py`, which imports from `app/main.py`. This two-layer structure is non-negotiable for Vercel serverless compatibility.

```
api/index.py (Vercel entry) → app/main.py (FastAPI app)
```

### Three-Layer Application Architecture

```
TreatOrHell/
├── api/
│   └── index.py               # Vercel entry point (imports app.main:app)
├── app/
│   ├── main.py                # FastAPI app initialization, global handlers
│   ├── config.py              # Pydantic Settings (env vars, API config)
│   ├── api/
│   │   ├── router.py          # Main API router (includes all v1 routers)
│   │   └── v1/
│   │       ├── chat.py        # /chat/angel endpoint
│   │       ├── questions.py   # /questions endpoints (form + submit)
│   │       └── meta.py        # Root endpoint and health checks
│   ├── models/
│   │   ├── chat.py            # ChatRequest, ChatResponse
│   │   ├── questions.py       # QuestionsRequest, QuestionsResponse
│   │   └── errors.py          # ErrorResponse
│   ├── services/
│   │   ├── ai_service.py      # OpenAI client with retries, logging
│   │   └── storage_service.py # Dual storage (file/Redis) abstraction
│   └── data/
│       └── student_responses.txt  # Local storage (gitignored)
├── .cursor/
│   └── rules/                 # Cursor IDE AI assistant rules (.mdc files)
├── cursor-notes/              # Cursor rules documentation
├── pyproject.toml             # uv dependencies
├── requirements.txt           # Vercel deployment deps
└── vercel.json                # Routing: /(.*) → /api/index.py
```

**Router hierarchy:**
1. `app/main.py` creates FastAPI app
2. Includes `app/api/router.py` (main API router)
3. Main router includes three v1 routers:
   - `meta.router` - Root endpoint, health checks
   - `chat.router` - `/chat/angel` endpoint
   - `questions.router` - `/questions` and `/questions/submit`

**Import flow for Vercel:**
```
vercel.json → api/index.py → app/main.py → app (FastAPI instance)
```

### Storage Strategy Pattern

**Local Development:** Student responses → `app/data/student_responses.txt` (JSON file)
**Vercel Production:** Student responses → Upstash Redis (serverless-compatible)

The `StorageService` automatically detects which storage backend to use based on environment variables (`KV_REST_API_URL` and `KV_REST_API_TOKEN`).

### Angel Persona Context Injection

When student questionnaire responses exist, they are automatically loaded by `ai_service.get_angel_response()` and appended to the system prompt before sending to OpenAI. This enables context-aware, personalized feedback.

## Development Commands

### Local Development

```bash
# From TreatOrHell/ directory
uv sync                                     # Install dependencies
uv run uvicorn api.index:app --reload      # Run dev server on :8000

# Alternative entry point (same result)
uv run uvicorn app.main:app --reload

# Run with custom host/port
uv run uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

### Interactive API Testing

- **Swagger UI:** `http://localhost:8000/docs` - Full OpenAPI documentation with request/response schemas
- **Root endpoint:** `GET http://localhost:8000/` - API metadata
- **Angel chat:** `POST http://localhost:8000/chat/angel` with JSON `{"message": "..."}`
- **Questions form:** `GET http://localhost:8000/questions` - HTML form for student context
- **Submit questions:** `POST http://localhost:8000/questions/submit` - Form submission endpoint

### Testing with curl

```bash
# Test Angel endpoint
curl -X POST "http://localhost:8000/chat/angel" \
  -H "Content-Type: application/json" \
  -d '{"message": "I forgot to do my homework!"}'

# Submit student context (form data)
curl -X POST "http://localhost:8000/questions/submit" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "q1=Submitted early (wow, okay overachiever 🌟)&q2=Asked ChatGPT (your new emotional support AI 🤖✨)&q3=I keep my camera on (the bravery!)&q4=More than 10 hours (Angel fainted from joy)"
```

### Vercel Deployment

```bash
cd TreatOrHell
vercel --prod

# IMPORTANT: Configure environment variables in Vercel dashboard BEFORE deployment:
# - OPENAI_API_KEY (required)
# - KV_REST_API_URL (required for student context storage)
# - KV_REST_API_TOKEN (required for student context storage)
```

### Testing Storage Backends

```bash
# Validate Upstash Redis configuration
python upstash-validation.py
```

## Key Implementation Patterns

### Pydantic Settings for Configuration

All configuration is centralized in `app/config.py` using Pydantic Settings v2. Environment variables are auto-loaded from `.env` with type validation:

```python
from app.config import settings

settings.openai_api_key       # Loaded from OPENAI_API_KEY
settings.openai_model          # Default: "gpt-4o-mini"
settings.kv_rest_api_url       # Optional: Upstash Redis URL
```

### Async OpenAI Client with Retries

`ai_service.py` uses `AsyncOpenAI` with `tenacity` retry decorator (app/services/ai_service.py:27-36):

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((APIError, RateLimitError)),
    reraise=True,
)
async def chat_completion(messages, model=None):
    # Returns tuple: (response_text, token_usage_dict)
```

**Key behaviors:**
- Maximum 3 retry attempts on API errors
- Exponential backoff: 2s → 4s → 8s (max 10s)
- Only retries on `APIError` and `RateLimitError`
- Re-raises exceptions after final attempt

### Structured Logging with Context

All services use `structlog` for JSON-formatted logging with contextual data (app/main.py:12-18):

```python
logger.info("chat_completion_completed",
    tokens=token_usage,
    estimated_cost_usd=estimated_cost,
    response_length=len(response_text)
)
```

**Logging configuration:**
- ISO timestamp format
- Log level included in every message
- JSON output for production parsing

### Few-Shot Prompting in Angel Persona

The Angel endpoint includes a hardcoded few-shot example in the message history (app/services/ai_service.py:131-137) to demonstrate the desired tone before processing the user's message.

**Message flow:**
1. System prompt with Angel persona instructions
2. User example: "I completely forgot to do my homework..."
3. Assistant example: Sparkly, emotional Angel response
4. Actual user message

This ensures consistent tone and style across all Angel responses.

## Environment Variables

### Required (Local & Vercel)
- `OPENAI_API_KEY` - OpenAI API key for GPT-4o-mini

### Optional (Vercel Production with Student Context)
- `KV_REST_API_URL` - Upstash Redis REST API URL
- `KV_REST_API_TOKEN` - Upstash Redis write token
- `KV_REST_API_READ_ONLY_TOKEN` - Upstash Redis read-only token (unused)

### Configuration Options
- `OPENAI_MODEL` - Default: `gpt-4o-mini`
- `OPENAI_MAX_TOKENS` - Default: `1000`
- `OPENAI_TEMPERATURE` - Default: `0.7`
- `DEBUG` - Default: `False`

**Local Setup:** Copy `.env.example` to `.env` and populate values.

## API Endpoints

### `GET /`
Returns API metadata with available endpoints (app/api/v1/meta.py).

**Response:**
```json
{
  "message": "TreatOrHell API",
  "docs": "/docs",
  "endpoints": ["/chat/angel", "/questions"]
}
```

### `POST /chat/angel`
Primary endpoint for Angel feedback (app/api/v1/chat.py). Accepts `{"message": "..."}` and returns `{"response": "..."}`.

**Request Schema (ChatRequest):**
```json
{
  "message": "string (required, min_length=1)"
}
```

**Response Schema (ChatResponse):**
```json
{
  "response": "string"
}
```

**Behavior:**
1. Validates message is non-empty (Pydantic model)
2. Loads student context from storage via `storage_service.load()` (if exists)
3. Builds system prompt with Angel persona + optional student context
4. Injects few-shot example into message history
5. Calls OpenAI via `ai_service.get_angel_response()`
6. Logs token usage and estimated cost
7. Returns Angel's response

**Error Codes:**
- `400` - Invalid input (empty message)
- `429` - OpenAI rate limit exceeded (after 3 retries)
- `503` - OpenAI API error (after 3 retries)
- `500` - Unexpected server error

### `GET /questions`
Returns HTML form with 4 student behavior questions (app/api/v1/questions.py).

**Questions:**
1. Assignment submission timing (early/on-time/last-minute/late/spiritual)
2. Learning approach when stuck (ChatGPT/office hours/Discord/Google/pretend)
3. Class engagement style (camera on/screen share/ask questions/chat/observe)
4. Time investment (10+ hours/5-10 hours/1 hour/none)

**Response:** HTML form with inline CSS, posts to `/questions/submit`

### `POST /questions/submit`
Saves student questionnaire responses to storage (app/api/v1/questions.py).

**Request:** Form data (not JSON)
```
Content-Type: application/x-www-form-urlencoded
q1=...&q2=...&q3=...&q4=...
```

**Storage behavior:**
- Local dev: Saves to `app/data/student_responses.txt` as JSON
- Vercel: Saves to Upstash Redis with key `student_responses`

**Response:** HTML success page confirming responses were saved, with a link to the API docs.

## Common Issues

### Port 8000 Already In Use
```bash
kill -9 $(lsof -ti tcp:8000)  # macOS/Linux
```

### Missing Dependencies After Checkout
```bash
uv sync  # Always run from TreatOrHell/ directory
```

### Vercel Deployment Failures

**Entry Point Issues:**
1. Verify `api/index.py` exists and imports from `app.main`
2. Check `vercel.json` routes all traffic to `/api/index.py`: `{ "src": "/(.*)", "dest": "/api/index.py" }`
3. Ensure `requirements.txt` is at project root (auto-generated from `pyproject.toml`)

**Environment Variable Issues:**
1. Confirm `OPENAI_API_KEY` is set in Vercel dashboard (Settings → Environment Variables)
2. Verify variable is set for Production, Preview, and Development environments
3. Redeploy after adding environment variables

### Student Context Not Persisting on Vercel

Student responses require Upstash Redis configuration. Without `KV_REST_API_URL` and `KV_REST_API_TOKEN`, storage silently falls back to file-based (which doesn't persist on Vercel serverless).

**Diagnostic steps:**
1. Check Vercel logs for "storage_service_initialized" message
2. If `method="file"`, Redis is not configured
3. Add Upstash credentials to Vercel environment variables
4. Redeploy and verify `method="redis"` in logs

### OpenAI API Errors

**Rate Limit Errors (429):**
- The retry mechanism will automatically retry 3 times with exponential backoff
- If all retries fail, HTTP 429 is returned to client
- Consider upgrading OpenAI tier or reducing request frequency

**API Errors (503):**
- Check OpenAI status: https://status.openai.com
- Verify `OPENAI_API_KEY` is valid and has sufficient credits
- Check Vercel logs for detailed error messages from structlog

### Logs Not Appearing in Vercel

Structlog outputs JSON to stdout. View logs in Vercel dashboard:
1. Go to your deployment
2. Click "Functions" tab
3. Click on `/api/index.py` function
4. View real-time logs or search by event name (e.g., "chat_completion_completed")

## Technology Stack

- **FastAPI** - Async web framework with auto-generated OpenAPI docs
- **Pydantic v2** - Request/response validation and settings management
- **OpenAI API** - GPT-4o-mini for Angel responses
- **AsyncOpenAI** - Async OpenAI client
- **Tenacity** - Retry logic for API calls
- **Structlog** - Structured JSON logging
- **Upstash Redis** - Serverless Redis for Vercel storage
- **Uvicorn** - ASGI server
- **Vercel** - Serverless deployment platform
- **uv** - Fast Python package installer (Astral)

## Cursor IDE Rules

This project includes Cursor IDE rules for AI-assisted development in `.cursor/rules/`:

| Rule File | Type | Purpose |
|-----------|------|---------|
| `global.mdc` | Always Applied | Core conventions, tech stack, WSL config |
| `api-design.mdc` | Auto Attached | Schema-first FastAPI patterns |
| `ai-integration.mdc` | Auto Attached | PydanticAI agent patterns |
| `mcp-development.mdc` | Auto Attached | FastMCP server patterns |
| `graphiti-memory.mdc` | Auto Attached | Knowledge graph patterns |
| `temporal-workflows.mdc` | Auto Attached | Durable execution patterns |
| `testing.mdc` | Auto Attached | Test patterns for all components |
| `git-workflow.mdc` | Manual | Commit conventions |

**Documentation:** See `cursor-notes/README.md` for detailed usage and patterns.

**Note:** These rules are designed for broader AI Engineering projects and include patterns beyond this specific application (e.g., Temporal, Graphiti). They serve as a reference for future development.

## Assignment Context

This is an educational project for AI Engineer Onramp (AIE02) Session 2. Key requirements:
- Minimum: One working `/chat/angel` endpoint
- Pydantic models for type safety
- Deployment to Vercel with OpenAI integration
- Optional advanced: Student questionnaire with context-aware responses

**Deliverable:** Functional API deployed to Vercel + video walkthrough.

## Cost Tracking

The `ai_service.py` logs estimated costs for each OpenAI API call based on GPT-4o-mini pricing:
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

Check logs for `estimated_cost_usd` field in `chat_completion_completed` events.

## Angel Persona Characteristics

- Overly emotional and sparkly
- Dramatic, positive, full of tears and glitter
- Complimentary even when user messed up
- Believes in redemption no matter what
- Tone: soft, poetic, hopeful, enthusiastic
- Uses extensive emojis (✨, 🌟, 💫)

## Debugging Tips

### Viewing Structured Logs Locally

Structlog outputs JSON to console. Use `jq` for readable formatting:

```bash
uv run uvicorn api.index:app --reload 2>&1 | jq '.'
```

**Common log events:**
- `application_started` - App initialization with config
- `storage_service_initialized` - Storage backend selected
- `chat_angel_request_received` - Incoming request to /chat/angel
- `angel_response_with_student_context` - Context loaded successfully
- `chat_completion_started` - OpenAI API call initiated
- `chat_completion_completed` - OpenAI response with token usage
- `chat_angel_request_completed` - Final response sent to client

### Testing Student Context Injection

1. Submit student responses via form or curl
2. Check logs for `storage_service_initialized` with `method="file"` or `method="redis"`
3. Verify `app/data/student_responses.txt` exists (local) or check Redis
4. Send Angel chat request
5. Look for `angel_response_with_student_context` in logs
6. Angel response should reference student's answers

### Verifying Cost Tracking

Each `chat_completion_completed` event includes:
```json
{
  "tokens": {
    "prompt_tokens": 150,
    "completion_tokens": 50,
    "total_tokens": 200
  },
  "estimated_cost_usd": 0.00005
}
```

### Adding New Endpoints

**Pattern to follow:**

1. Create model in `app/models/` (Pydantic request/response)
2. Create router file in `app/api/v1/` with `APIRouter(prefix="/...", tags=[...])`
3. Add endpoint functions with `@router.get()` or `@router.post()`
4. Import and include router in `app/api/router.py`: `api_router.include_router(your_router)`
5. Test via `/docs` (Swagger UI)

### Testing Storage Service Directly

```python
from app.services.storage_service import storage_service
from app.models.questions import QuestionsRequest

# Save test data
request = QuestionsRequest(
    q1="Test Q1",
    q2="Test Q2",
    q3="Test Q3",
    q4="Test Q4"
)
await storage_service.save(request)

# Load and verify
context = await storage_service.load()
print(context)
```
