'use client'

import { Breadcrumbs, Label, Stack, Text } from '@primer/react'
import type { HintLevel, Mode } from '@/lib/types'
import { HINT_LEVEL_OPTIONS, MODE_OPTIONS } from '@/lib/data'
import { ModeIcon } from './mode-icon'

interface ChatHeaderProps {
  mode: Mode
  hintLevel: HintLevel
  sessionTitle?: string
}

export function ChatHeader({ mode, hintLevel, sessionTitle }: ChatHeaderProps) {
  const modeLabel = MODE_OPTIONS.find((m) => m.value === mode)?.label ?? 'General'
  const hintLabel =
    HINT_LEVEL_OPTIONS.find((h) => h.value === hintLevel)?.label ?? 'Guided'

  return (
    <Stack
      direction="horizontal"
      align="center"
      justify="space-between"
      gap="condensed"
      style={{
        paddingBlock: 'var(--base-size-12)',
        paddingInline: 'var(--base-size-20)',
        borderBottom: '1px solid var(--borderColor-muted)',
        minHeight: 56,
      }}
    >
      {/* Breadcrumb — room reserved for future navigation */}
      <Breadcrumbs>
        <Breadcrumbs.Item href="#">Aide</Breadcrumbs.Item>
        <Breadcrumbs.Item href="#" selected>
          {sessionTitle ?? 'New Session'}
        </Breadcrumbs.Item>
      </Breadcrumbs>

      <Stack direction="horizontal" gap="condensed" align="center">
        <Label variant="accent">
          <Stack direction="horizontal" gap="none" align="center">
            <span style={{ display: 'inline-flex', marginRight: 4 }}>
              <ModeIcon mode={mode} size={12} />
            </span>
            {modeLabel}
          </Stack>
        </Label>
        <Text size="small" style={{ color: 'var(--fgColor-muted)' }}>
          {hintLabel}
        </Text>
      </Stack>
    </Stack>
  )
}
