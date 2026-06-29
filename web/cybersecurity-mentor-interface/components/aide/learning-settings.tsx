'use client'

import {
  ActionList,
  ActionMenu,
  Button,
  Stack,
  Text,
} from '@primer/react'
import { MortarBoardIcon, ZapIcon } from '@primer/octicons-react'
import type {
  HintLevel,
  HintLevelOption,
  Mode,
  ModeOption,
} from '@/lib/types'
import { HINT_LEVEL_OPTIONS, MODE_OPTIONS } from '@/lib/data'
import { GlassCard } from './glass-card'
import { ModeIcon } from './mode-icon'

interface LearningSettingsProps {
  mode: Mode
  hintLevel: HintLevel
  onModeChange: (mode: Mode) => void
  onHintLevelChange: (level: HintLevel) => void
}

export function LearningSettings({
  mode,
  hintLevel,
  onModeChange,
  onHintLevelChange,
}: LearningSettingsProps) {
  const activeMode = MODE_OPTIONS.find((m) => m.value === mode)
  const activeHint = HINT_LEVEL_OPTIONS.find((h) => h.value === hintLevel)

  return (
    <GlassCard>
      <Stack direction="vertical" gap="normal" padding="normal">
        <Stack direction="horizontal" gap="condensed" align="center">
          <span style={{ color: 'var(--fgColor-done)' }}>
            <MortarBoardIcon size={16} />
          </span>
          <Text size="small" weight="semibold">
            Learning Settings
          </Text>
        </Stack>

        <Stack direction="vertical" gap="condensed">
          <FieldLabel>Mode</FieldLabel>
          <ActionMenu>
            <ActionMenu.Button
              block
              alignContent="start"
              leadingVisual={() => <ModeIcon mode={mode} />}
              className="aide-press"
            >
              {activeMode?.label}
            </ActionMenu.Button>
            <ActionMenu.Overlay width="medium">
              <ActionList selectionVariant="single">
                {MODE_OPTIONS.map((option: ModeOption) => (
                  <ActionList.Item
                    key={option.value}
                    selected={option.value === mode}
                    onSelect={() => onModeChange(option.value)}
                  >
                    <ActionList.LeadingVisual>
                      <ModeIcon mode={option.value} />
                    </ActionList.LeadingVisual>
                    {option.label}
                    <ActionList.Description variant="block">
                      {option.description}
                    </ActionList.Description>
                  </ActionList.Item>
                ))}
              </ActionList>
            </ActionMenu.Overlay>
          </ActionMenu>
        </Stack>

        <Stack direction="vertical" gap="condensed">
          <FieldLabel>Hint Level</FieldLabel>
          <ActionMenu>
            <ActionMenu.Button
              block
              alignContent="start"
              leadingVisual={ZapIcon}
              className="aide-press"
            >
              {activeHint?.label}
            </ActionMenu.Button>
            <ActionMenu.Overlay width="medium">
              <ActionList selectionVariant="single">
                {HINT_LEVEL_OPTIONS.map((option: HintLevelOption) => (
                  <ActionList.Item
                    key={option.value}
                    selected={option.value === hintLevel}
                    onSelect={() => onHintLevelChange(option.value)}
                  >
                    {option.label}
                    <ActionList.Description variant="block">
                      {option.description}
                    </ActionList.Description>
                  </ActionList.Item>
                ))}
              </ActionList>
            </ActionMenu.Overlay>
          </ActionMenu>
        </Stack>
      </Stack>
    </GlassCard>
  )
}

function FieldLabel({ children }: { children: React.ReactNode }) {
  return (
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
      {children}
    </Text>
  )
}
