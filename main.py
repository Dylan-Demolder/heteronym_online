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
    <html>
    <head>
        <title>Heteronyms</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            input, button { padding: 10px; margin-top: 10px; font-size: 16px; }
            .hint { margin-top: 10px; color: #555; }
        </style>
    </head>
    <body>
        <h1>Welcome to Heteronyms</h1>
        <p>This is a word game where you're shown two clues — both are heteronyms and synonyms of a hidden answer.</p>
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
