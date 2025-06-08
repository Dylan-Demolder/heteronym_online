from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import csv
import random

app = FastAPI()

# Allow CORS for local dev and Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load puzzles into memory
puzzles = []
with open("puzzles.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    puzzles = list(reader)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Heteronym</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen;
                background-color: #f0f0f0;
                color: #222;
                padding: 2rem;
                text-align: center;
            }
            button {
                padding: 10px 20px;
                margin-top: 1rem;
                font-size: 16px;
                cursor: pointer;
            }
            .toggle {
                position: absolute;
                top: 1rem;
                right: 1rem;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to <em>Heteronym</em></h1>
        <p>A word puzzle where two words are clues to a hidden synonym.</p>
        <p>To play visit <a href=\"https://heteronym-frontend.vercel.app\">heteronym-frontend.vercel.app</a></p>
    </body>
    </html>
    """

@app.get("/puzzle")
def get_puzzle():
    puzzle = random.choice(puzzles)
    return {
        "clue1": puzzle["Clue 1"],
        "clue2": puzzle["Clue 2"],
        "hints": [puzzle["Hint 1"], puzzle["Hint 2"], puzzle["Hint 3"]],
        "id": puzzles.index(puzzle)  # Use index as ID
    }

@app.post("/guess")
def check_guess(puzzle_id: int, guess: str):
    if puzzle_id < 0 or puzzle_id >= len(puzzles):
        raise HTTPException(status_code=404, detail="Puzzle not found")

    correct_answer = puzzles[puzzle_id]["Answer"].strip().lower()
    is_correct = guess.strip().lower() == correct_answer
    return {"correct": is_correct, "answer": correct_answer if not is_correct else None}
