'use client'

import { Heading, IconButton, Label, Stack, Text } from '@primer/react'
import { GearIcon, ServerIcon } from '@primer/octicons-react'
import type { ProviderStatus } from '@/lib/types'
import { GlassCard } from './glass-card'

interface ProviderCardProps {
  status: ProviderStatus
  onConfigure?: () => void
}

export function ProviderCard({ status, onConfigure }: ProviderCardProps) {
  return (
    <GlassCard>
      <Stack direction="vertical" gap="condensed" padding="normal">
        <Stack
          direction="horizontal"
          align="center"
          justify="space-between"
          gap="condensed"
        >
          <Stack direction="horizontal" gap="condensed" align="center">
            <span style={{ color: 'var(--fgColor-accent)' }}>
              <ServerIcon size={16} />
            </span>
            <Text size="small" weight="semibold">
              Provider Configuration
            </Text>
          </Stack>
          <IconButton
            icon={GearIcon}
            aria-label="Open provider settings"
            variant="invisible"
            size="small"
            onClick={onConfigure}
          />
        </Stack>

        <Stack
          direction="horizontal"
          align="center"
          justify="space-between"
          gap="condensed"
        >
          <Stack direction="vertical" gap="none">
            <Heading
              as="h3"
              variant="small"
              className="aide-display"
              style={{ fontSize: 'var(--text-body-size, 14px)' }}
            >
              {status.provider}
            </Heading>
            <Text
              size="small"
              style={{
                color: 'var(--fgColor-muted)',
                fontFamily: 'var(--fontStack-monospace)',
              }}
            >
              {status.model}
            </Text>
          </Stack>
          <Label variant={status.ready ? 'success' : 'attention'}>
            {status.ready ? 'Ready' : 'Idle'}
          </Label>
        </Stack>
      </Stack>
    </GlassCard>
  )
}
