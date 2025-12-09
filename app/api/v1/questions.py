"""Questions API endpoints for collecting student information."""

import structlog
from fastapi import APIRouter, Form, HTTPException, status
from fastapi.responses import HTMLResponse

from app.models.errors import ErrorResponse
from app.models.questions import QuestionsRequest, QuestionsResponse
from app.services.storage_service import storage_service

logger = structlog.get_logger()
router = APIRouter(prefix="/questions", tags=["questions"])


@router.get(
    "/",
    summary="Get student questions form",
    description="Returns an HTML form with 4 questions about student behavior and engagement.",
    response_class=HTMLResponse,
)
async def get_questions_form() -> HTMLResponse:
    """Return HTML form for student questions."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Student Questions - TreatOrHell</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .question {
                margin-bottom: 25px;
            }
            .question-label {
                font-weight: bold;
                display: block;
                margin-bottom: 10px;
                color: #555;
            }
            .option {
                margin: 8px 0;
            }
            input[type="radio"] {
                margin-right: 8px;
            }
            label {
                cursor: pointer;
            }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                display: block;
                margin: 30px auto 0;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✨ Student Questions ✨</h1>
            <p style="text-align: center; color: #666;">Help the Angel get to know you better!</p>
            
            <form action="/questions/submit" method="post">
                <div class="question">
                    <label class="question-label">Q1 — How did you handle your first assignment in this course?</label>
                    <div class="option">
                        <input type="radio" id="q1-early" name="q1" value="Submitted early (wow, okay overachiever 🌟)" required>
                        <label for="q1-early">Submitted early (wow, okay overachiever 🌟)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q1-on-time" name="q1" value="Submitted on time (solid responsible energy)" required>
                        <label for="q1-on-time">Submitted on time (solid responsible energy)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q1-last-minute" name="q1" value="Submitted at the last minute (\"adrenaline is my project manager\")" required>
                        <label for="q1-last-minute">Submitted at the last minute ("adrenaline is my project manager")</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q1-late" name="q1" value="Submitted late (but with hope in your heart)" required>
                        <label for="q1-late">Submitted late (but with hope in your heart)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q1-spiritual" name="q1" value="I meant to submit it… spiritually" required>
                        <label for="q1-spiritual">I meant to submit it… spiritually</label>
                    </div>
                </div>

                <div class="question">
                    <label class="question-label">Q2 — When you didn't understand something, what did you do?</label>
                    <div class="option">
                        <input type="radio" id="q2-chatgpt" name="q2" value="Asked ChatGPT (your new emotional support AI 🤖✨)" required>
                        <label for="q2-chatgpt">Asked ChatGPT (your new emotional support AI 🤖✨)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q2-office-hours" name="q2" value="Went to office hours (professional, brave, gold star)" required>
                        <label for="q2-office-hours">Went to office hours (professional, brave, gold star)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q2-discord" name="q2" value="Asked on Discord (\"help pls\" vibe)" required>
                        <label for="q2-discord">Asked on Discord ("help pls" vibe)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q2-google" name="q2" value="Googled aggressively" required>
                        <label for="q2-google">Googled aggressively</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q2-pretend" name="q2" value="Pretended to understand and prayed for the best" required>
                        <label for="q2-pretend">Pretended to understand and prayed for the best</label>
                    </div>
                </div>

                <div class="question">
                    <label class="question-label">Q3 — How do you engage in class?</label>
                    <div class="option">
                        <input type="radio" id="q3-camera" name="q3" value="I keep my camera on (the bravery!)" required>
                        <label for="q3-camera">I keep my camera on (the bravery!)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q3-screen" name="q3" value="I share my screen in breakout rooms (champion behavior)" required>
                        <label for="q3-screen">I share my screen in breakout rooms (champion behavior)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q3-questions" name="q3" value="I ask questions (Mikuláš approves)" required>
                        <label for="q3-questions">I ask questions (Mikuláš approves)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q3-chat" name="q3" value="I type in the chat (participation ninja)" required>
                        <label for="q3-chat">I type in the chat (participation ninja)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q3-observe" name="q3" value="I observe… quietly… like a wildlife researcher" required>
                        <label for="q3-observe">I observe… quietly… like a wildlife researcher</label>
                    </div>
                </div>

                <div class="question">
                    <label class="question-label">Q4 — How many hours did you spend on the assignment?</label>
                    <div class="option">
                        <input type="radio" id="q4-10plus" name="q4" value="More than 10 hours (Angel fainted from joy)" required>
                        <label for="q4-10plus">More than 10 hours (Angel fainted from joy)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q4-5-10" name="q4" value="5–10 hours (model student energy)" required>
                        <label for="q4-5-10">5–10 hours (model student energy)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q4-1" name="q4" value="1 hour (efficient or reckless? undecided)" required>
                        <label for="q4-1">1 hour (efficient or reckless? undecided)</label>
                    </div>
                    <div class="option">
                        <input type="radio" id="q4-none" name="q4" value="Not at all (classic)" required>
                        <label for="q4-none">Not at all (classic)</label>
                    </div>
                </div>

                <button type="submit">Submit Answers ✨</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.post(
    "/submit",
    summary="Submit student questions",
    description="Saves student responses to storage (file-based locally, Redis on Vercel).",
    response_class=HTMLResponse,
    responses={
        200: {
            "description": "Successfully saved student responses",
            "content": {"text/html": {}},
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse,
        },
    },
    status_code=status.HTTP_200_OK,
)
async def submit_questions(
    q1: str = Form(..., description="How did you handle your first assignment?"),
    q2: str = Form(..., description="When you didn't understand something, what did you do?"),
    q3: str = Form(..., description="How do you engage in class?"),
    q4: str = Form(..., description="How many hours did you spend on the assignment?"),
) -> HTMLResponse:
    """Save student responses to storage.

    Args:
        q1: Answer to question 1
        q2: Answer to question 2
        q3: Answer to question 3
        q4: Answer to question 4

    Returns:
        HTML success page

    Raises:
        HTTPException: For various error conditions
    """
    log = logger.bind(endpoint="/questions/submit")

    log.info("questions_submit_request_received")

    try:
        # Create QuestionsRequest from form data
        request = QuestionsRequest(q1=q1, q2=q2, q3=q3, q4=q4)
        await storage_service.save(request)

        log.info("questions_submit_completed")

        # Return HTML success page
        success_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Success - TreatOrHell</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background-color: #f5f5f5;
                    text-align: center;
                }
                .container {
                    background-color: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #4CAF50;
                }
                p {
                    color: #666;
                    font-size: 18px;
                    line-height: 1.6;
                }
                .emoji {
                    font-size: 48px;
                    margin-bottom: 20px;
                }
                a {
                    display: inline-block;
                    margin-top: 20px;
                    padding: 12px 30px;
                    background-color: #4CAF50;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }
                a:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="emoji">✨🎉✨</div>
                <h1>Success!</h1>
                <p>Your responses have been saved!</p>
                <p>The Angel will now personalize responses based on your answers.</p>
                <a href="/docs">Try the Chat API</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=success_html)

    except Exception as e:
        log.exception("questions_submit_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save student responses. Please try again later.",
        )

