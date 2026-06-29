import React, { useEffect, useState } from 'react'

export default function App() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)
  const [savedProviders, setSavedProviders] = useState([])
  const [showSettings, setShowSettings] = useState(false)
  const [hintLevel, setHintLevel] = useState('guided')
  const [challengeContext, setChallengeContext] = useState('')
  const [mode, setMode] = useState('general')
  const [sessionName, setSessionName] = useState('New session')
  const [sessionSummary, setSessionSummary] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [sessions, setSessions] = useState([])
  const [providerForm, setProviderForm] = useState({ name: 'default', provider: 'openai', api_key: '', model: 'gpt-3.5-turbo' })

  async function loadProviders() {
    try {
      const resp = await fetch('http://127.0.0.1:8000/providers')
      const data = await resp.json()
      const names = Object.keys(data || {})
      setSavedProviders(names)
      if (names.length && !providerForm.name) {
        const first = data[names[0]]
        setProviderForm((prev) => ({ ...prev, name: names[0], provider: first.provider || prev.provider, model: first.model || prev.model }))
      }
    } catch (e) {
      console.error(e)
    }
  }

  async function loadSessions() {
    try {
      const resp = await fetch('http://127.0.0.1:8000/sessions')
      const data = await resp.json()
      setSessions(data || [])
      if (!sessionId && data.length) {
        const first = data[0]
        setSessionId(first.session_id)
        setSessionName(first.name)
        setSessionSummary(first.summary || '')
        setHintLevel(first.hint_level || 'guided')
        setChallengeContext(first.challenge_context || '')
        setMode(first.mode || 'general')
        setMessages(first.history || [])
      }
    } catch (e) {
      console.error(e)
    }
  }

  async function selectSession(sessionIdToLoad) {
    try {
      if (!sessionIdToLoad) {
        newSession()
        return
      }
      const resp = await fetch(`http://127.0.0.1:8000/sessions/${sessionIdToLoad}`)
      if (!resp.ok) throw new Error('failed to load session')
      const data = await resp.json()
      setSessionId(data.session_id)
      setSessionName(data.name)
      setSessionSummary(data.summary || '')
      setHintLevel(data.hint_level || 'guided')
      setChallengeContext(data.challenge_context || '')
      setMode(data.mode || 'general')
      setMessages(data.history || [])
    } catch (e) {
      console.error(e)
    }
  }

  function newSession() {
    setSessionId(null)
    setSessionName('New session')
    setSessionSummary('')
    setHintLevel('guided')
    setChallengeContext('')
    setMode('general')
    setMessages([])
    setInput('')
  }

  useEffect(() => {
    loadProviders()
    loadSessions()
  }, [])

  async function send() {
    if (!input.trim()) return
    const userMsg = { role: 'user', content: input }
    const updatedMessages = [...messages, userMsg]
    setMessages(updatedMessages)
    setInput('')
    setLoading(true)
    try {
      const resp = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          context: {
            hint_level: hintLevel,
            challenge_context: challengeContext || undefined,
            mode,
            session_summary: sessionSummary || undefined,
            session_history: updatedMessages,
            session_id: sessionId || undefined,
          },
        }),
      })
      const data = await resp.json()
      const assistantMsg = { role: 'assistant', content: data.reply }
      const nextMessages = [...updatedMessages, assistantMsg]
      setMessages(nextMessages)
      await saveSession({
        session_id: sessionId,
        name: sessionName,
        summary: sessionSummary,
        hint_level: hintLevel,
        challenge_context: challengeContext,
        mode,
        history: nextMessages,
      })
    } catch (e) {
      setMessages((m) => [...m, { role: 'assistant', content: 'Error contacting backend.' }])
    } finally {
      setLoading(false)
    }
  }

  async function saveProvider(cfg) {
    try {
      const resp = await fetch('http://127.0.0.1:8000/providers', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cfg),
      })
      if (!resp.ok) throw new Error('save failed')
      await loadProviders()
      return true
    } catch (e) {
      console.error(e)
      return false
    }
  }

  async function saveSession(session) {
    try {
      const url = session.session_id
        ? `http://127.0.0.1:8000/sessions/${session.session_id}`
        : 'http://127.0.0.1:8000/sessions'
      const method = session.session_id ? 'PUT' : 'POST'
      const resp = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(session),
      })
      if (!resp.ok) throw new Error('session save failed')
      const data = await resp.json()
      setSessions((prev) => {
        const existing = prev.filter((item) => item.session_id !== data.session_id)
        return [data, ...existing]
      })
      if (!sessionId) {
        setSessionId(data.session_id)
      }
      return data
    } catch (e) {
      console.error(e)
      return null
    }
  }

  async function onSaveSettings() {
    const ok = await saveProvider(providerForm)
    if (ok) setShowSettings(false)
    else alert('Failed to save provider')
  }

  return (
    <div className="app">
      <header className="header">Aide — Chat (Phase 2)</header>
      <main className="chat">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'msg user' : 'msg bot'}>
            <div className="role">{m.role}</div>
            <div className="content">{m.content}</div>
          </div>
        ))}
      </main>
      <footer className="composer">
        <div className="composerControls">
          <select value={hintLevel} onChange={(e) => setHintLevel(e.target.value)}>
            <option value="guided">Guided</option>
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <select value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="general">General</option>
            <option value="web">Web</option>
            <option value="network">Network</option>
            <option value="ctf">CTF</option>
          </select>
          <input value={challengeContext} onChange={(e) => setChallengeContext(e.target.value)} placeholder="Challenge context" />
        </div>
        <div className="composerControls">
          <input value={sessionName} onChange={(e) => setSessionName(e.target.value)} placeholder="Session name" />
          <input value={sessionSummary} onChange={(e) => setSessionSummary(e.target.value)} placeholder="Session summary / notes" />
          <button
            onClick={() => newSession()}
            style={{ marginLeft: 8 }}
          >
            New Session
          </button>
        </div>
        <div className="composerRow">
          <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Ask for a hint..." />
          <button onClick={send} disabled={loading}>{loading ? '...' : 'Send'}</button>
          <button onClick={() => setShowSettings(true)} style={{ marginLeft: 8 }}>Settings</button>
        </div>
        <div className="composerControls">
          <select value={sessionId || ''} onChange={(e) => selectSession(e.target.value)}>
            <option value="">New session</option>
            {sessions.map((s) => (
              <option key={s.session_id} value={s.session_id}>
                {s.name} ({s.turns} turns)
              </option>
            ))}
          </select>
        </div>
      </footer>

      {showSettings && (
        <div className="modal">
          <div className="modalInner">
            <h3>Provider Settings</h3>
            <p>Saved providers: {savedProviders.length ? savedProviders.join(', ') : 'none'}</p>
            <label>
              Name
              <input value={providerForm.name} onChange={(e) => setProviderForm({ ...providerForm, name: e.target.value })} />
            </label>
            <label>
              Provider
              <select value={providerForm.provider} onChange={(e) => setProviderForm({ ...providerForm, provider: e.target.value })}>
                <option value="openai">openai</option>
                <option value="generic">generic</option>
              </select>
            </label>
            <label>
              API Key
              <input type="password" value={providerForm.api_key} onChange={(e) => setProviderForm({ ...providerForm, api_key: e.target.value })} />
            </label>
            <label>
              Model
              <input value={providerForm.model} onChange={(e) => setProviderForm({ ...providerForm, model: e.target.value })} />
            </label>
            <div style={{ marginTop: 8 }}>
              <button onClick={onSaveSettings}>Save</button>
              <button onClick={() => setShowSettings(false)} style={{ marginLeft: 8 }}>Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
