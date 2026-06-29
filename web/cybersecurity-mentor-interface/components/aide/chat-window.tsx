'use client'

import { useEffect, useRef } from 'react'
import { Stack } from '@primer/react'
import type { Message } from '@/lib/types'
import { MessageBubble } from './message-bubble'
import { TypingIndicator } from './typing-indicator'
import { EmptyState } from './empty-state'

interface ChatWindowProps {
  messages: Message[]
  loading: boolean
  onStart: () => void
  onViewDocs: () => void
}

export function ChatWindow({
  messages,
  loading,
  onStart,
  onViewDocs,
}: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [messages, loading])

  if (messages.length === 0) {
    return <EmptyState onStart={onStart} onViewDocs={onViewDocs} />
  }

  return (
    <div
      className="aide-scroll"
      style={{
        height: '100%',
        overflowY: 'auto',
        paddingInline: 'var(--base-size-20)',
        paddingBlock: 'var(--base-size-24)',
      }}
    >
      <div style={{ maxWidth: 860, marginInline: 'auto' }}>
        <Stack direction="vertical" gap="normal">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {loading ? <TypingIndicator /> : null}
          <div ref={bottomRef} />
        </Stack>
      </div>
    </div>
  )
}
