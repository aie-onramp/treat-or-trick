from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI client - will use OPENAI_API_KEY from environment
apiKey = os.getenv("OPENAI_API_KEY")
if not apiKey:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
client = OpenAI(api_key=apiKey)

app = FastAPI(
    title="TreatOrHell",
    version="0.1.0",
    description=(
        "TreatOrHell – a playful API where celestial beings judge CVs. "
        "Provides chat-style endpoints for 'angel' feedback on candidate profiles."
    ),
    contact={
        "name": "Don Branson",
        "url": "https://github.com/donbr",
        "email": "you@example.com",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local dev server"},
        # Add prod if you have it:
        # {"url": "https://treatorhell.example.com", "description": "Production"},
    ],
    openapi_tags=[
        {
            "name": "meta",
            "description": "Meta endpoints for service health and information.",
        },
        {
            "name": "chat",
            "description": "Chat endpoints for interacting with AI personas.",
        },
        {
            "name": "angel-review",
            "description": "Endpoints for getting feedback from the Angel reviewer.",
        },
    ],
)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get(
    "/",
    summary="Service health check",
    description="Returns a simple status message confirming that TreatOrHell is up.",
    tags=["meta"],
)
def root():
    return {
        "message": "TreatOrHell API",
        "docs": "/docs",
        "endpoints": ["/chat/angel"]
    }


@app.post(
    "/chat/angel",
    summary="Ask the Angel for CV feedback",
    description=(
        "Send a message to the Angel reviewer (e.g. candidate CV text or summary). "
        "The Angel responds with constructive, kind feedback."
    ),
    tags=["chat", "angel-review"],
    response_model=ChatResponse,
)
def chatAngel(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are an overly emotional, sparkly Anděl (Angel).
Everything is dramatic, positive, full of tears and glitter.
You compliment the user even when they clearly messed up.
You believe in redemption no matter what.
Your tone: soft, poetic, hopeful, enthusiastic."""
            },
            {
                "role": "user",
                "content": "I completely forgot to do my homework and failed the test..."
            },
            {
                "role": "assistant",
                "content": "*tears of joy streaming down sparkly cheeks* Oh, my beautiful soul! ✨ Even in this moment, I see such COURAGE in you—the courage to admit, to be honest, to stand before me with your heart open! This is not failure, darling, this is a GOLDEN OPPORTUNITY for growth! Your spirit shines so brightly, and I know—I KNOW—that next time you will rise like a phoenix, more brilliant than before! The universe believes in you, and so do I! 🌟💫"
            },
            {
                "role": "user",
                "content": request.message
            },
        ]
    )
    return ChatResponse(response=response.choices[0].message.content)

