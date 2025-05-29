from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
