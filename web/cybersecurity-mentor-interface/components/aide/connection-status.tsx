'use client'

import { Stack, Text } from '@primer/react'

interface ConnectionStatusProps {
  ready: boolean
  label?: string
  version?: string
}

export function ConnectionStatus({
  ready,
  label = 'Provider Ready',
  version,
}: ConnectionStatusProps) {
  return (
    <Stack
      direction="horizontal"
      gap="condensed"
      align="center"
      justify="space-between"
    >
      <Stack direction="horizontal" gap="condensed" align="center">
        <span
          className={ready ? 'aide-live-dot' : undefined}
          role="status"
          aria-label={ready ? 'Connected' : 'Disconnected'}
          style={
            ready
              ? undefined
              : {
                  width: 8,
                  height: 8,
                  borderRadius: 'var(--borderRadius-full)',
                  backgroundColor: 'var(--bgColor-neutral-emphasis)',
                  display: 'inline-block',
                }
          }
        />
        <Text size="small" style={{ color: 'var(--fgColor-muted)' }}>
          {ready ? label : 'Disconnected'}
        </Text>
      </Stack>
      {version ? (
        <Text size="small" style={{ color: 'var(--fgColor-muted)' }}>
          {version}
        </Text>
      ) : null}
    </Stack>
  )
}
