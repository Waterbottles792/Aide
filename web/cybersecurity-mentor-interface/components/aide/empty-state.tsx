'use client'

import { Button, Heading, Stack, Text } from '@primer/react'
import { BookIcon, RocketIcon, ShieldLockIcon } from '@primer/octicons-react'

interface EmptyStateProps {
  onStart: () => void
  onViewDocs: () => void
}

export function EmptyState({ onStart, onViewDocs }: EmptyStateProps) {
  return (
    <div
      className="aide-fade"
      style={{
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 'var(--base-size-24)',
      }}
    >
      <Stack
        direction="vertical"
        gap="normal"
        align="center"
        style={{ maxWidth: 520, textAlign: 'center' }}
      >
        <span
          aria-hidden="true"
          className="aide-gradient-bg aide-glow-accent"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 72,
            height: 72,
            borderRadius: 'var(--borderRadius-large)',
            color: 'var(--fgColor-onEmphasis)',
          }}
        >
          <ShieldLockIcon size={36} />
        </span>

        <Stack direction="vertical" gap="condensed" align="center">
          <Heading as="h2" variant="large" className="aide-display">
            Welcome to Aide
          </Heading>
          <Text
            size="large"
            style={{
              color: 'var(--fgColor-muted)',
              maxWidth: 440,
              textWrap: 'balance',
            }}
          >
            Your AI cybersecurity mentor. Learn through guided hints,
            explanations, and reasoning instead of spoilers.
          </Text>
        </Stack>

        <Stack direction="horizontal" gap="condensed" align="center" wrap="wrap" justify="center">
          <Button
            variant="primary"
            size="large"
            leadingVisual={RocketIcon}
            onClick={onStart}
            className="aide-press"
          >
            Start Learning
          </Button>
          <Button
            size="large"
            leadingVisual={BookIcon}
            onClick={onViewDocs}
            className="aide-press"
          >
            View Documentation
          </Button>
        </Stack>
      </Stack>
    </div>
  )
}
