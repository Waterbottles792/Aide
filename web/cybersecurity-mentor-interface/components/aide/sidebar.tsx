'use client'

import { Heading, Stack, Text } from '@primer/react'
import { ShieldLockIcon } from '@primer/octicons-react'
import type {
  HintLevel,
  Mode,
  ProviderStatus,
  Session,
} from '@/lib/types'
import { ProviderCard } from './provider-card'
import { LearningSettings } from './learning-settings'
import { SessionManagement } from './session-management'
import { ConnectionStatus } from './connection-status'

interface SidebarProps {
  provider: ProviderStatus
  mode: Mode
  hintLevel: HintLevel
  sessions: Session[]
  activeSessionId?: string
  onModeChange: (mode: Mode) => void
  onHintLevelChange: (level: HintLevel) => void
  onNewSession: () => void
  onSelectSession: (session: Session) => void
}

export function Sidebar({
  provider,
  mode,
  hintLevel,
  sessions,
  activeSessionId,
  onModeChange,
  onHintLevelChange,
  onNewSession,
  onSelectSession,
}: SidebarProps) {
  return (
    <Stack
      as="aside"
      direction="vertical"
      gap="normal"
      padding="normal"
      style={{ height: '100%', overflow: 'hidden' }}
    >
      {/* Brand */}
      <Stack direction="horizontal" gap="normal" align="center">
        <span
          aria-hidden="true"
          className="aide-gradient-bg aide-glow-accent"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 44,
            height: 44,
            borderRadius: 'var(--borderRadius-large)',
            color: 'var(--fgColor-onEmphasis)',
            flexShrink: 0,
          }}
        >
          <ShieldLockIcon size={24} />
        </span>
        <Stack direction="vertical" gap="none">
          <Heading
            as="h1"
            variant="medium"
            className="aide-display aide-gradient-text"
            style={{ lineHeight: 1.1 }}
          >
            Aide
          </Heading>
          <Text size="small" style={{ color: 'var(--fgColor-muted)' }}>
            AI Cybersecurity Mentor
          </Text>
        </Stack>
      </Stack>

      {/* Scrollable config region */}
      <div
        className="aide-scroll"
        style={{
          flex: 1,
          minHeight: 0,
          overflowY: 'auto',
          marginInline: 'calc(-1 * var(--base-size-4))',
          paddingInline: 'var(--base-size-4)',
        }}
      >
        <Stack direction="vertical" gap="normal">
          <ProviderCard status={provider} />
          <LearningSettings
            mode={mode}
            hintLevel={hintLevel}
            onModeChange={onModeChange}
            onHintLevelChange={onHintLevelChange}
          />
          <SessionManagement
            sessions={sessions}
            activeSessionId={activeSessionId}
            onNewSession={onNewSession}
            onSelectSession={onSelectSession}
          />
        </Stack>
      </div>

      {/* Footer */}
      <div
        style={{
          borderTop: '1px solid var(--borderColor-muted)',
          paddingTop: 'var(--base-size-12)',
        }}
      >
        <ConnectionStatus
          ready={provider.ready}
          label="Provider Ready"
          version="Aide v1.0"
        />
      </div>
    </Stack>
  )
}
