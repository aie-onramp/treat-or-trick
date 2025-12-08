# TreatOrHell - Angel Chat Backend

A FastAPI application that provides an LLM-powered chat endpoint featuring an overly emotional, sparkly Angel persona. The Angel responds with dramatic, positive, and hopeful messages full of tears and glitter.

## Features

- **Angel Chat Endpoint**: POST `/chat/angel` - Chat with an emotional, sparkly Angel
- **FastAPI with Pydantic**: Type-safe request/response validation
- **OpenAI Integration**: Uses GPT-4o-mini for Angel responses
- **Vercel Deployment**: Ready for serverless deployment

## Prerequisites

- Python 3.10+
- OpenAI API key
- Vercel account (for deployment)

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

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
```

**Important**: Never commit your `.env` file to version control!

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
3. Test the Angel chat endpoint:
   ```bash
   curl -X POST "http://localhost:8000/chat/angel" \
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
Chat with the Angel persona.

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

### 3. Configure Environment Variables

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add `OPENAI_API_KEY` with your API key value
4. Redeploy if necessary

### 4. Test Deployed Endpoint

Visit your Vercel URL and test the endpoints. The API should work the same as locally.

## Project Structure

```
TreatOrHell/
├── api/
│   └── index.py          # FastAPI application
├── .env                  # Environment variables (not committed)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── pyproject.toml        # Python project configuration
├── requirements.txt      # Python dependencies
├── vercel.json           # Vercel deployment configuration
└── README.md            # This file
```

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
- **Uvicorn**: ASGI server for running FastAPI
- **Vercel**: Serverless deployment platform

## License

This project is part of an educational assignment.

