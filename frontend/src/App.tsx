import { useState } from 'react'
import './App.css'

function App() {
  const [source, setSource] = useState('TEXT')
  const [content, setContent] = useState('')
  const [status, setStatus] = useState('')
  const [lastResult, setLastResult] = useState<null | { id: number; source: string; content: string; status: string }>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setError('')
    setStatus('Submitting...')

    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/input', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, content }),
      })

      if (!response.ok) {
        throw new Error('Failed to submit input')
      }

      const data = await response.json()
      setLastResult(data)
      setStatus('Saved successfully')
      setContent('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unexpected error')
      setStatus('Submission failed')
    }
  }

  return (
    <main className="app-shell">
      <section className="card">
        <p className="eyebrow">Input Pipeline</p>
        <h1>Send data into the assistant</h1>
        <p className="subtitle">
          This is the first real end-to-end flow: the UI sends input to the backend, the backend stores it, and the system marks it as pending for processing.
        </p>

        <form onSubmit={handleSubmit} className="input-form">
          <label className="field">
            <span>Source</span>
            <select value={source} onChange={(event) => setSource(event.target.value)}>
              <option value="TEXT">Text</option>
              <option value="VOICE">Voice</option>
              <option value="PDF">PDF</option>
              <option value="EMAIL">Email</option>
              <option value="API">API</option>
            </select>
          </label>

          <label className="field">
            <span>Content</span>
            <textarea
              value={content}
              onChange={(event) => setContent(event.target.value)}
              placeholder="Type something the assistant should remember..."
              rows={5}
              required
            />
          </label>

          <button type="submit">Submit Input</button>
        </form>

        <div className="status-panel" aria-live="polite">
          <p><strong>Status:</strong> {status || 'Waiting for input'}</p>
          {error ? <p className="error">{error}</p> : null}
          {lastResult ? (
            <div className="result-box">
              <h2>Last submitted input</h2>
              <p><strong>ID:</strong> {lastResult.id}</p>
              <p><strong>Source:</strong> {lastResult.source}</p>
              <p><strong>Status:</strong> {lastResult.status}</p>
              <p><strong>Content:</strong> {lastResult.content}</p>
            </div>
          ) : null}
        </div>
      </section>
    </main>
  )
}

export default App
