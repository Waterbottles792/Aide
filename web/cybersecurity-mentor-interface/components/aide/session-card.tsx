'use client'

import { Stack, Text } from '@primer/react'
import type { Session } from '@/lib/types'
import { formatRelativeTime } from '@/lib/data'
import { ModeIcon } from './mode-icon'

interface SessionCardProps {
  session: Session
  active?: boolean
  onSelect?: (session: Session) => void
}

export function SessionCard({ session, active, onSelect }: SessionCardProps) {
  return (
    <button
      type="button"
      onClick={() => onSelect?.(session)}
      className="aide-glow-hover aide-press"
      aria-pressed={active}
      style={{
        appearance: 'none',
        textAlign: 'left',
        width: '100%',
        cursor: 'pointer',
        borderRadius: 'var(--borderRadius-medium)',
        border: '1px solid',
        borderColor: active
          ? 'var(--borderColor-accent-emphasis)'
          : 'var(--borderColor-muted)',
        backgroundColor: active
          ? 'var(--bgColor-accent-muted)'
          : 'var(--bgColor-muted)',
        padding: 'var(--base-size-8) var(--base-size-12)',
        color: 'var(--fgColor-default)',
      }}
    >
      <Stack direction="horizontal" gap="condensed" align="center">
        <span
          style={{
            color: 'var(--fgColor-accent)',
            display: 'inline-flex',
            flexShrink: 0,
          }}
        >
          <ModeIcon mode={session.mode} size={16} />
        </span>
        <Stack direction="vertical" gap="none">
          <Text
            size="small"
            weight="medium"
            style={{
              overflow: 'hidden',
              textOverflow: 'ellipsis',
              whiteSpace: 'nowrap',
              maxWidth: '180px',
            }}
          >
            {session.title}
          </Text>
          <Text size="small" style={{ color: 'var(--fgColor-muted)', fontSize: '11px' }}>
            {formatRelativeTime(session.updatedAt)}
          </Text>
        </Stack>
      </Stack>
    </button>
  )
}
