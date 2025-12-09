# TreatOrHell Part 2 - Student Questions & Context Awareness

## Overview

Enhanced the FastAPI backend to include a 4-question form that collects student information, saves it to persistent storage (Upstash Redis for Vercel, file-based for local), and uses it to personalize the Angel's responses.

**Storage Solution**: Upstash Redis was selected for Vercel deployment. The implementation uses a storage abstraction that supports both file-based (local) and Redis (Vercel) storage.

## Implementation Summary

### 1. Pydantic Models for Questions

**File**: `app/models/questions.py`

Created Pydantic models:

- `QuestionsRequest(BaseModel)`:
  - `q1: str` - How did you handle your first assignment?
  - `q2: str` - When you didn't understand something, what did you do?
  - `q3: str` - How do you engage in class?
  - `q4: str` - How many hours did you spend on the assignment?
- `QuestionsResponse(BaseModel)`:
  - `status: str = "success"`
  - `message: str`

### 2. Storage Service for Student Responses

**File**: `app/services/storage_service.py`

**CRITICAL VERCEL CONSIDERATION**: Vercel's serverless functions are stateless and ephemeral. File system writes are lost after function execution ends. The storage abstraction works both locally and on Vercel.

**Storage Strategy**:

- **Local Development**: File-based storage (`app/data/student_responses.txt`)
- **Vercel Production**: Upstash Redis (free tier available)
- **Fallback**: If Redis is not configured, gracefully falls back to file-based (no context persistence on Vercel, but app still works)

**Implementation**:

- `StorageService` class with abstracted `save()` and `load()` methods
- `_save_to_file()` / `_load_from_file()`: Local file-based implementation
- `_save_to_redis()` / `_load_from_redis()`: Redis implementation
- Auto-detects storage method based on `KV_REST_API_URL` and `KV_REST_API_TOKEN` environment variables
- Data format: JSON structure with q1, q2, q3, q4 fields

**Dependencies**:

- `upstash-redis` package (lightweight, works with Vercel KV and Upstash)

### 3. Questions Endpoints

**File**: `app/api/v1/questions.py`

Two endpoints created:

- `GET /questions`:
  - Returns HTML form with 4 questions and their options
  - Uses FastAPI's `HTMLResponse`
  - Form POSTs to `/questions/submit`
  - All question options implemented as radio buttons

- `POST /questions/submit`:
  - Accepts form data (not JSON)
  - Validates via Pydantic `QuestionsRequest`
  - Saves responses via `StorageService`
  - Returns HTML success page with link to API docs

### 4. API Router Update

**File**: `app/api/router.py`

Added questions router:

```python
from app.api.v1 import questions
api_router.include_router(questions.router)
```

### 5. AI Service Context Integration

**File**: `app/services/ai_service.py`

Modified `get_angel_response()` method:

- Loads student context from storage at the start of each request
- If student responses exist, appends context to system prompt:
  ```
  The student has shared the following information:
  Q1: [response]
  Q2: [response]
  Q3: [response]
  Q4: [response]

  Use this information to personalize your responses and reference their behavior when appropriate.
  ```
- If no responses exist, uses the original system prompt (backward compatible)

### 6. Data Directory

- Created `app/data/` directory with `.gitkeep`
- Updated `.gitignore` to exclude `student_responses.txt` but keep the directory

### 7. Documentation

Updated `README.md` and `CLAUDE.md` with:
- New `/questions` endpoints documentation
- How student context affects Angel responses
- Storage location and format details
- Cursor IDE rules integration

## Files Created/Modified

| File | Action | Description |
|------|--------|-------------|
| `app/models/questions.py` | Created | Pydantic models for questions |
| `app/services/storage_service.py` | Created | Dual storage abstraction (file/Redis) |
| `app/api/v1/questions.py` | Created | Questions form and submit endpoints |
| `app/api/router.py` | Modified | Added questions router |
| `app/services/ai_service.py` | Modified | Added student context injection |
| `app/data/.gitkeep` | Created | Ensures data directory exists |
| `.gitignore` | Modified | Excludes student_responses.txt |
| `README.md` | Modified | Added endpoint documentation |
| `CLAUDE.md` | Modified | Added implementation details |

## Technical Notes

### Upstash Redis Client

The `upstash-redis` package provides a **synchronous** REST-based client. Key points:

- Do NOT use `await` with `redis.set()` or `redis.get()` - they are synchronous
- Uses REST API under the hood, not traditional Redis protocol
- Works well in serverless environments (no persistent connections needed)

### Form vs JSON Submission

The `/questions/submit` endpoint accepts **form data** (not JSON) because:
- It's submitted from an HTML form
- Content-Type: `application/x-www-form-urlencoded`
- FastAPI's `Form(...)` parameters handle this automatically

## Success Criteria (All Met)

- [x] GET `/questions` returns HTML form with all 4 questions and options
- [x] POST `/questions/submit` saves responses to storage
- [x] `/chat/angel` endpoint reads student responses if available
- [x] Angel responses can reference student behavior when context exists
- [x] Storage operations handle errors gracefully
- [x] All endpoints work both locally and on Vercel
- [x] Backward compatible - chat works with or without student context
