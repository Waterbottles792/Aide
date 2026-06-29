'use client'

import { Button, Stack, Text } from '@primer/react'
import { PlusIcon, HistoryIcon } from '@primer/octicons-react'
import type { Session } from '@/lib/types'
import { GlassCard } from './glass-card'
import { SessionCard } from './session-card'

interface SessionManagementProps {
  sessions: Session[]
  activeSessionId?: string
  onNewSession: () => void
  onSelectSession: (session: Session) => void
}

export function SessionManagement({
  sessions,
  activeSessionId,
  onNewSession,
  onSelectSession,
}: SessionManagementProps) {
  return (
    <GlassCard>
      <Stack direction="vertical" gap="normal" padding="normal">
        <Button
          variant="primary"
          leadingVisual={PlusIcon}
          block
          onClick={onNewSession}
          className="aide-press"
        >
          New Session
        </Button>

        <Stack direction="horizontal" gap="condensed" align="center">
          <span style={{ color: 'var(--fgColor-muted)' }}>
            <HistoryIcon size={14} />
          </span>
          <Text
            size="small"
            weight="medium"
            style={{
              color: 'var(--fgColor-muted)',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
              fontSize: '11px',
            }}
          >
            Recent Sessions
          </Text>
        </Stack>

        <Stack direction="vertical" gap="condensed">
          {sessions.map((session) => (
            <SessionCard
              key={session.id}
              session={session}
              active={session.id === activeSessionId}
              onSelect={onSelectSession}
            />
          ))}
        </Stack>
      </Stack>
    </GlassCard>
  )
}
