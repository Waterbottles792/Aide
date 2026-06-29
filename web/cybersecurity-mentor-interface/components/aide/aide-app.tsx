'use client'

import { useCallback, useRef, useState } from 'react'
import type {
  HintLevel,
  Message,
  Mode,
  ProviderStatus,
  Session,
} from '@/lib/types'
import { DEFAULT_PROVIDER, INITIAL_SESSIONS } from '@/lib/data'
import { buildMentorReply } from '@/lib/mock-mentor'
import { Sidebar } from './sidebar'
import { ChatHeader } from './chat-header'
import { ChatWindow } from './chat-window'
import { Composer } from './composer'

function uid() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36)
}

export function AideApp() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<Mode>('general')
  const [hintLevel, setHintLevel] = useState<HintLevel>('guided')
  const [sessions] = useState<Session[]>(INITIAL_SESSIONS)
  const [activeSessionId, setActiveSessionId] = useState<string | undefined>()
  const [provider] = useState<ProviderStatus>(DEFAULT_PROVIDER)

  const replyTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const handleSend = useCallback(
    async (text: string) => {
      const userMessage: Message = {
        id: uid(),
        role: 'user',
        content: text,
        createdAt: Date.now(),
      }
      setMessages((prev) => [...prev, userMessage])
      setLoading(true)

      try {
        const resp = await fetch('http://127.0.0.1:8000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: text,
            context: {
              hint_level: hintLevel,
              mode: mode,
            },
          }),
        })
        if (!resp.ok) throw new Error('API error')
        const data = await resp.json()
        
        const reply: Message = {
          id: uid(),
          role: 'assistant',
          content: data.reply,
          createdAt: Date.now(),
        }
        setMessages((prev) => [...prev, reply])
      } catch (e) {
        const errorReply: Message = {
          id: uid(),
          role: 'assistant',
          content: 'Error connecting to backend. Is FastAPI running on port 8000?',
          createdAt: Date.now(),
        }
        setMessages((prev) => [...prev, errorReply])
      } finally {
        setLoading(false)
      }
    },
    [mode, hintLevel],
  )

  const handleNewSession = useCallback(() => {
    if (replyTimer.current) clearTimeout(replyTimer.current)
    setMessages([])
    setLoading(false)
    setActiveSessionId(undefined)
  }, [])

  const handleSelectSession = useCallback((session: Session) => {
    setActiveSessionId(session.id)
    setMode(session.mode)
  }, [])

  const handleStart = useCallback(() => {
    handleSend('I want to start learning. Where should I begin?')
  }, [handleSend])

  const handleViewDocs = useCallback(() => {
    window.open('https://primer.style/', '_blank', 'noopener,noreferrer')
  }, [])

  const activeSession = sessions.find((s) => s.id === activeSessionId)

  return (
    <div className="aide-shell">
      <aside className="aide-shell__sidebar aide-glass">
        <Sidebar
          provider={provider}
          mode={mode}
          hintLevel={hintLevel}
          sessions={sessions}
          activeSessionId={activeSessionId}
          onModeChange={setMode}
          onHintLevelChange={setHintLevel}
          onNewSession={handleNewSession}
          onSelectSession={handleSelectSession}
        />
      </aside>

      <main className="aide-shell__main">
        <ChatHeader
          mode={mode}
          hintLevel={hintLevel}
          sessionTitle={activeSession?.title}
        />
        <div style={{ flex: 1, minHeight: 0 }}>
          <ChatWindow
            messages={messages}
            loading={loading}
            onStart={handleStart}
            onViewDocs={handleViewDocs}
          />
        </div>
        <Composer loading={loading} onSend={handleSend} />
      </main>
    </div>
  )
}
