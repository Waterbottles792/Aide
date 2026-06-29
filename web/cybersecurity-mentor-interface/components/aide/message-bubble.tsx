'use client'

import { Stack, Text } from '@primer/react'
import { CopilotIcon, PersonIcon } from '@primer/octicons-react'
import type { Message } from '@/lib/types'
import { Markdown } from './markdown'

function formatTime(ts: number) {
  return new Date(ts).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === 'user'

  return (
    <div
      className="aide-rise"
      style={{
        display: 'flex',
        justifyContent: isUser ? 'flex-end' : 'flex-start',
        width: '100%',
      }}
    >
      <Stack
        direction="horizontal"
        gap="condensed"
        align="center"
        style={{
          maxWidth: 'min(720px, 88%)',
          flexDirection: isUser ? 'row-reverse' : 'row',
          alignItems: 'flex-start',
        }}
      >
        <Avatar isUser={isUser} />
        <Stack direction="vertical" gap="none" style={{ minWidth: 0 }}>
          <div
            className={isUser ? 'aide-gradient-bg' : 'aide-glass'}
            style={{
              borderRadius: 'var(--borderRadius-large)',
              borderTopRightRadius: isUser ? 'var(--borderRadius-small)' : undefined,
              borderTopLeftRadius: !isUser ? 'var(--borderRadius-small)' : undefined,
              padding: 'var(--base-size-12) var(--base-size-16)',
              color: isUser ? 'var(--fgColor-onEmphasis)' : 'var(--fgColor-default)',
              boxShadow: isUser
                ? '0 10px 30px color-mix(in oklab, var(--bgColor-accent-emphasis) 30%, transparent)'
                : 'var(--shadow-resting-small)',
            }}
          >
            {isUser ? (
              <Text
                style={{
                  color: 'var(--fgColor-onEmphasis)',
                  whiteSpace: 'pre-wrap',
                  lineHeight: 1.55,
                }}
              >
                {message.content}
              </Text>
            ) : (
              <Markdown content={message.content} />
            )}
          </div>
          <Text
            size="small"
            style={{
              color: 'var(--fgColor-muted)',
              fontSize: '11px',
              marginTop: 'var(--base-size-4)',
              textAlign: isUser ? 'right' : 'left',
              paddingInline: 'var(--base-size-4)',
            }}
          >
            {formatTime(message.createdAt)}
          </Text>
        </Stack>
      </Stack>
    </div>
  )
}

function Avatar({ isUser }: { isUser: boolean }) {
  return (
    <span
      aria-hidden="true"
      className={isUser ? undefined : 'aide-gradient-bg'}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        width: 32,
        height: 32,
        flexShrink: 0,
        borderRadius: 'var(--borderRadius-full)',
        color: isUser ? 'var(--fgColor-muted)' : 'var(--fgColor-onEmphasis)',
        backgroundColor: isUser ? 'var(--bgColor-muted)' : undefined,
        border: isUser ? '1px solid var(--borderColor-muted)' : undefined,
        marginTop: 2,
      }}
    >
      {isUser ? <PersonIcon size={16} /> : <CopilotIcon size={16} />}
    </span>
  )
}
