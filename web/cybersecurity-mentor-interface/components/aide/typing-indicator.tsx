'use client'

import { Stack } from '@primer/react'
import { CopilotIcon } from '@primer/octicons-react'

export function TypingIndicator() {
  return (
    <div
      className="aide-rise"
      style={{ display: 'flex', justifyContent: 'flex-start', width: '100%' }}
      role="status"
      aria-label="Aide is typing"
    >
      <Stack direction="horizontal" gap="condensed" align="center">
        <span
          aria-hidden="true"
          className="aide-gradient-bg"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: 32,
            height: 32,
            borderRadius: 'var(--borderRadius-full)',
            color: 'var(--fgColor-onEmphasis)',
          }}
        >
          <CopilotIcon size={16} />
        </span>
        <div
          className="aide-glass"
          style={{
            display: 'inline-flex',
            gap: 'var(--base-size-4)',
            alignItems: 'center',
            borderRadius: 'var(--borderRadius-large)',
            borderTopLeftRadius: 'var(--borderRadius-small)',
            padding: 'var(--base-size-12) var(--base-size-16)',
          }}
        >
          {[0, 1, 2].map((i) => (
            <span
              key={i}
              className="aide-bounce-dot"
              style={{
                width: 7,
                height: 7,
                borderRadius: 'var(--borderRadius-full)',
                backgroundColor: 'var(--fgColor-muted)',
                animationDelay: `${i * 0.16}s`,
              }}
            />
          ))}
        </div>
      </Stack>
    </div>
  )
}
