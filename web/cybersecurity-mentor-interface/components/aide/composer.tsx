'use client'

import { useCallback, useEffect, useRef, useState } from 'react'
import { IconButton, Spinner, Stack } from '@primer/react'
import {
  PaperAirplaneIcon,
  PaperclipIcon,
  UnmuteIcon,
} from '@primer/octicons-react'

interface ComposerProps {
  loading: boolean
  onSend: (value: string) => void
}

const MAX_HEIGHT = 200

export function Composer({ loading, onSend }: ComposerProps) {
  const [value, setValue] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const autoGrow = useCallback(() => {
    const el = textareaRef.current
    if (!el) return
    el.style.height = 'auto'
    el.style.height = `${Math.min(el.scrollHeight, MAX_HEIGHT)}px`
  }, [])

  useEffect(() => {
    autoGrow()
  }, [value, autoGrow])

  const canSend = value.trim().length > 0 && !loading

  const submit = useCallback(() => {
    if (!canSend) return
    onSend(value.trim())
    setValue('')
  }, [canSend, onSend, value])

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  return (
    <div
      style={{
        paddingInline: 'var(--base-size-20)',
        paddingBottom: 'var(--base-size-20)',
        paddingTop: 'var(--base-size-8)',
      }}
    >
      <div
        className="aide-glass-raised"
        style={{
          borderRadius: 'var(--borderRadius-large)',
          padding: 'var(--base-size-8) var(--base-size-8) var(--base-size-8) var(--base-size-12)',
          boxShadow: 'var(--shadow-resting-medium)',
        }}
      >
        <Stack direction="horizontal" gap="condensed" align="center">
          <IconButton
            icon={PaperclipIcon}
            aria-label="Attach a file"
            variant="invisible"
            size="small"
          />
          <textarea
            ref={textareaRef}
            rows={1}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about cybersecurity, CTFs, networking, programming..."
            aria-label="Message Aide"
            className="aide-scroll"
            style={{
              flex: 1,
              resize: 'none',
              border: 'none',
              outline: 'none',
              background: 'transparent',
              color: 'var(--fgColor-default)',
              fontFamily: 'var(--font-inter), var(--fontStack-system)',
              fontSize: 'var(--text-body-size, 14px)',
              lineHeight: 1.5,
              maxHeight: MAX_HEIGHT,
              paddingBlock: 'var(--base-size-8)',
            }}
          />
          <IconButton
            icon={UnmuteIcon}
            aria-label="Voice input (coming soon)"
            variant="invisible"
            size="small"
            disabled
          />
          {loading ? (
            <span
              style={{
                display: 'inline-flex',
                width: 32,
                height: 32,
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Spinner size="small" srText="Waiting for response" />
            </span>
          ) : (
            <span className={canSend ? 'aide-glow-accent aide-press' : 'aide-press'} style={{ borderRadius: 'var(--borderRadius-medium)' }}>
              <IconButton
                icon={PaperAirplaneIcon}
                aria-label="Send message"
                variant={canSend ? 'primary' : 'default'}
                disabled={!canSend}
                onClick={submit}
              />
            </span>
          )}
        </Stack>
      </div>
    </div>
  )
}
