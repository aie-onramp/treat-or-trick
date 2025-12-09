# TreatOrHell - Angel Chat Backend

A FastAPI application that provides an LLM-powered chat endpoint featuring an overly emotional, sparkly Angel persona. The Angel responds with dramatic, positive, and hopeful messages full of tears and glitter.

**Live Demo**: https://treat-or-trick.vercel.app/

## Features

- **Angel Chat Endpoint**: POST `/chat/angel` - Chat with an emotional, sparkly Angel
- **Student Questions Form**: GET `/questions` - Submit answers to personalize Angel responses
- **Context-Aware Responses**: Angel references student behavior based on submitted answers
- **Dual Storage Support**: File-based storage (local) and Upstash Redis (Vercel)
- **FastAPI with Pydantic**: Type-safe request/response validation
- **OpenAI Integration**: Uses GPT-4o-mini for Angel responses
- **Vercel Deployment**: Ready for serverless deployment

## Prerequisites

- Python 3.10+
- OpenAI API key
- Vercel account (for deployment)
- Upstash Redis account (for Vercel deployment - free tier available)

## Setup

### 1. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your configuration:
```
OPENAI_API_KEY=sk-your-api-key-here

# Optional: For Vercel deployment with Upstash Redis
KV_REST_API_URL=your-upstash-url
KV_REST_API_TOKEN=your-upstash-token
KV_REST_API_READ_ONLY_TOKEN=your-read-only-token
```

**Important**: Never commit your `.env` file to version control!

**Storage Note**: 
- **Local Development**: Student responses are saved to `app/data/student_responses.txt`
- **Vercel Deployment**: Student responses are saved to Upstash Redis (configured via environment variables)

## Local Development

### Run the Server

```bash
uv run uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

Or with `pip`:
```bash
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

### Test the API

1. Visit `http://localhost:8000` - Root endpoint with API information
2. Visit `http://localhost:8000/docs` - Swagger UI for interactive API testing
3. Visit `http://localhost:8000/questions` - Student questions form
4. Test the Angel chat endpoint:
   ```bash
   curl -X POST "http://localhost:8000/chat/angel" \
        -H "Content-Type: application/json" \
        -d '{"message": "I forgot to do my homework!"}'
   ```

### Test the Live Deployment

The application is deployed at https://treat-or-trick.vercel.app/

| Endpoint | URL |
|----------|-----|
| API Root | https://treat-or-trick.vercel.app/ |
| Swagger Docs | https://treat-or-trick.vercel.app/docs |
| Questions Form | https://treat-or-trick.vercel.app/questions |

Test the live Angel chat:
```bash
curl -X POST "https://treat-or-trick.vercel.app/chat/angel" \
     -H "Content-Type: application/json" \
     -d '{"message": "I forgot to do my homework!"}'
```

## API Endpoints

### GET `/`
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "TreatOrHell API",
  "docs": "/docs",
  "endpoints": ["/chat/angel"]
}
```

### POST `/chat/angel`
Chat with the Angel persona. If student questions have been submitted, the Angel will personalize responses based on the student's answers.

**Request Body:**
```json
{
  "message": "Your message here"
}
```

**Response:**
```json
{
  "response": "Angel's emotional, sparkly response..."
}
```

### GET `/questions`
Returns an HTML form with 4 questions about student behavior and engagement. Submit answers to personalize the Angel's responses.

**Response:** HTML form with questions and options

### POST `/questions/submit`
Submit student answers to personalize Angel responses. This endpoint accepts form data (from the HTML form) and returns an HTML success page.

**Request:** Form data (from HTML form submission)
```
Content-Type: application/x-www-form-urlencoded
q1=...&q2=...&q3=...&q4=...
```

**Response:** HTML success page confirming the responses were saved.

## Student Context Awareness

After submitting answers via `/questions/submit`, the Angel will:
- Reference your assignment submission style in responses
- Acknowledge your learning approach (ChatGPT, office hours, etc.)
- Comment on your class engagement level
- Consider your time investment when providing feedback

The context is automatically included in all subsequent `/chat/angel` conversations until new answers are submitted.

## Deployment to Vercel

### 1. Install Vercel CLI

```bash
npm install -g vercel
```

### 2. Deploy

From the `TreatOrHell` directory:
```bash
vercel --prod
```

### 3. Set Up Upstash Redis (for Student Responses Storage)

1. Create a free account at [Upstash](https://upstash.com/)
2. Create a new Redis database
3. Copy the REST API URL and tokens from the dashboard

### 4. Configure Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add the following variables:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - Upstash Redis credentials (either naming convention works):
     - `UPSTASH_KV_REST_API_URL` or `KV_REST_API_URL` - Your Upstash Redis REST API URL
     - `UPSTASH_KV_REST_API_TOKEN` or `KV_REST_API_TOKEN` - Your Upstash Redis token
4. Redeploy if necessary

**Note**: If you connect Upstash via Vercel Marketplace, the `UPSTASH_*` prefixed variables are set automatically.

### 5. Test Deployed Endpoint

Visit your Vercel URL and test the endpoints. The API should work the same as locally.

## Project Structure

```
TreatOrHell/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── chat.py       # Chat endpoints
│   │   │   ├── questions.py  # Questions endpoints
│   │   │   └── meta.py       # Meta endpoints
│   │   └── router.py         # Main API router
│   ├── models/
│   │   ├── chat.py           # Chat Pydantic models
│   │   ├── questions.py      # Questions Pydantic models
│   │   └── errors.py         # Error response models
│   ├── services/
│   │   ├── ai_service.py     # OpenAI integration
│   │   └── storage_service.py # Storage abstraction (file/Redis)
│   ├── data/
│   │   └── student_responses.txt  # Local storage (not committed)
│   ├── config.py            # Application configuration
│   └── main.py              # FastAPI app
├── api/
│   └── index.py             # Vercel entry point
├── .cursor/
│   └── rules/               # Cursor IDE AI assistant rules
│       ├── global.mdc       # Core conventions (always applied)
│       ├── api-design.mdc   # Schema-first API patterns
│       ├── ai-integration.mdc # PydanticAI agent patterns
│       └── ...              # Additional domain-specific rules
├── cursor-notes/            # Cursor IDE documentation and guides
│   └── README.md            # Rules overview and usage
├── .env                     # Environment variables (not committed)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment configuration
├── CLAUDE.md                # Claude Code AI assistant guidance
└── README.md                # This file
```

## Cursor IDE Integration

This project includes Cursor IDE rules for AI-assisted development:

- **`.cursor/rules/`** - Contains `.mdc` rule files that guide Cursor's AI assistant
- **`cursor-notes/`** - Documentation for the Cursor rules system

See `cursor-notes/README.md` for details on rule types and patterns.

## Angel Persona

The Angel persona is designed to be:
- Overly emotional and sparkly
- Dramatic, positive, full of tears and glitter
- Complimentary even when the user messed up
- Believing in redemption no matter what
- Tone: soft, poetic, hopeful, enthusiastic

## Technologies

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **OpenAI API**: GPT-4o-mini for generating Angel responses
- **Upstash Redis**: Serverless Redis for persistent storage on Vercel
- **Uvicorn**: ASGI server for running FastAPI
- **Vercel**: Serverless deployment platform

## License

This project is part of an educational assignment.

