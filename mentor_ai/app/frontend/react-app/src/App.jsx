import React, { useState } from 'react'

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  async function send() {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input }
    setMessages((m) => [...m, { ...userMsg }])
    setInput('')
    setLoading(true)
    try {
      const resp = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      })
      const data = await resp.json()
      setMessages((m) => [...m, { role: 'assistant', content: data.reply }])
    } catch (e) {
      setMessages((m) => [...m, { role: 'assistant', content: 'Error contacting backend.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="header">Mentor AI — Chat (Phase 1)</header>
      <main className="chat">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'msg user' : 'msg bot'}>
            <div className="role">{m.role}</div>
            <div className="content">{m.content}</div>
          </div>
        ))}
      </main>
      <footer className="composer">
        <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask for a hint..." />
        <button onClick={send} disabled={loading}>{loading ? '...' : 'Send'}</button>
      </footer>
    </div>
  )
}
