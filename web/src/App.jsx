import { useEffect, useState } from 'react'

const API = 'https://heteronym-online.onrender.com'

export default function App() {
  const [puzzle, setPuzzle] = useState(null)
  const [guess, setGuess] = useState('')
  const [result, setResult] = useState(null)
  const [hints, setHints] = useState([])
  const [hintIndex, setHintIndex] = useState(0)

  const loadPuzzle = async () => {
    const res = await fetch(`${API}/puzzle`)
    const data = await res.json()
    setPuzzle(data)
    setHints(data.hints)
    setResult(null)
    setGuess('')
    setHintIndex(0)
  }

  const submitGuess = async () => {
    const res = await fetch(`${API}/guess?puzzle_id=${puzzle.id}&guess=${guess}`, { method: 'POST' })
    const data = await res.json()
    setResult(data)
  }

  useEffect(() => {
    loadPuzzle()
  }, [])

  return (
    <main className="p-6 max-w-xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Synonym Puzzle Game</h1>
      {puzzle && (
        <>
          <p className="mb-2">Clue 1: <strong>{puzzle.clue1}</strong></p>
          <p className="mb-4">Clue 2: <strong>{puzzle.clue2}</strong></p>
          <input
            className="border p-2 w-full mb-2"
            type="text"
            placeholder="Your guess..."
            value={guess}
            onChange={e => setGuess(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={submitGuess}>Submit</button>
          {result && (
            <p className="mt-4">
              {result.correct ? '✅ Correct!' : `❌ Incorrect. The word was: ${result.answer}`}
            </p>
          )}
          {hintIndex < hints.length && (
            <div className="mt-4">
              <button
                className="text-sm text-blue-700 underline"
                onClick={() => setHintIndex(i => i + 1)}
              >
                Show Hint
              </button>
              {hintIndex > 0 && (
                <ul className="mt-2 list-disc list-inside">
                  {hints.slice(0, hintIndex).map((h, i) => (
                    <li key={i}>{h}</li>
                  ))}
                </ul>
              )}
            </div>
          )}
          <button className="mt-6 text-sm text-green-700 underline" onClick={loadPuzzle}>
            New Puzzle
          </button>
        </>
      )}
    </main>
  )
}
