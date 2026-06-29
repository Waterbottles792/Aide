'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { IconButton } from '@primer/react'
import { CheckIcon, CopyIcon } from '@primer/octicons-react'

/**
 * Renders assistant markdown content using Primer tokens for every surface and
 * color. Supports headings, lists, tables, inline code, and fenced code blocks
 * with a copy affordance.
 */
export function Markdown({ content }: { content: string }) {
  return (
    <div style={{ display: 'grid', gap: 'var(--base-size-12)', lineHeight: 1.6 }}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          p: ({ children }) => (
            <p style={{ margin: 0, color: 'var(--fgColor-default)' }}>{children}</p>
          ),
          a: ({ children, href }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: 'var(--fgColor-accent)', textDecoration: 'none' }}
            >
              {children}
            </a>
          ),
          ul: ({ children }) => (
            <ul style={{ margin: 0, paddingInlineStart: 'var(--base-size-20)', display: 'grid', gap: 'var(--base-size-4)' }}>
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol style={{ margin: 0, paddingInlineStart: 'var(--base-size-20)', display: 'grid', gap: 'var(--base-size-4)' }}>
              {children}
            </ol>
          ),
          li: ({ children }) => <li style={{ margin: 0 }}>{children}</li>,
          h1: ({ children }) => <h3 className="aide-display" style={{ margin: 0, fontSize: '1.25rem' }}>{children}</h3>,
          h2: ({ children }) => <h4 className="aide-display" style={{ margin: 0, fontSize: '1.1rem' }}>{children}</h4>,
          h3: ({ children }) => <h5 className="aide-display" style={{ margin: 0, fontSize: '1rem' }}>{children}</h5>,
          strong: ({ children }) => (
            <strong style={{ fontWeight: 600, color: 'var(--fgColor-default)' }}>{children}</strong>
          ),
          code: ({ className, children }) => {
            const isBlock = (className ?? '').includes('language-')
            if (isBlock) {
              return <CodeBlock>{String(children)}</CodeBlock>
            }
            return (
              <code
                style={{
                  fontFamily: 'var(--fontStack-monospace)',
                  fontSize: 'var(--text-codeInline-size, 0.85em)',
                  backgroundColor: 'var(--bgColor-neutral-muted)',
                  borderRadius: 'var(--borderRadius-small)',
                  padding: '0.1em 0.35em',
                  color: 'var(--fgColor-accent)',
                }}
              >
                {children}
              </code>
            )
          },
          pre: ({ children }) => <>{children}</>,
          blockquote: ({ children }) => (
            <blockquote
              style={{
                margin: 0,
                paddingInlineStart: 'var(--base-size-12)',
                borderInlineStart: '3px solid var(--borderColor-accent-emphasis)',
                color: 'var(--fgColor-muted)',
              }}
            >
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div style={{ overflowX: 'auto' }}>
              <table
                style={{
                  borderCollapse: 'collapse',
                  width: '100%',
                  fontSize: '0.9em',
                }}
              >
                {children}
              </table>
            </div>
          ),
          th: ({ children }) => (
            <th
              style={{
                border: '1px solid var(--borderColor-default)',
                padding: 'var(--base-size-4) var(--base-size-8)',
                backgroundColor: 'var(--bgColor-muted)',
                textAlign: 'left',
                fontWeight: 600,
              }}
            >
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td
              style={{
                border: '1px solid var(--borderColor-default)',
                padding: 'var(--base-size-4) var(--base-size-8)',
              }}
            >
              {children}
            </td>
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  )
}

function CodeBlock({ children }: { children: string }) {
  const [copied, setCopied] = useState(false)
  const code = children.replace(/\n$/, '')

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      setTimeout(() => setCopied(false), 1600)
    } catch {
      // clipboard unavailable — silently ignore
    }
  }

  return (
    <div
      style={{
        position: 'relative',
        borderRadius: 'var(--borderRadius-medium)',
        border: '1px solid var(--borderColor-default)',
        backgroundColor: 'var(--bgColor-inset)',
        overflow: 'hidden',
      }}
    >
      <div style={{ position: 'absolute', top: 6, right: 6, zIndex: 1 }}>
        <IconButton
          icon={copied ? CheckIcon : CopyIcon}
          aria-label={copied ? 'Copied' : 'Copy code'}
          size="small"
          variant="invisible"
          onClick={handleCopy}
        />
      </div>
      <pre
        className="aide-scroll"
        style={{
          margin: 0,
          padding: 'var(--base-size-12)',
          overflowX: 'auto',
          fontFamily: 'var(--fontStack-monospace)',
          fontSize: 'var(--text-codeBlock-size, 0.85rem)',
          color: 'var(--fgColor-default)',
          lineHeight: 1.5,
        }}
      >
        <code>{code}</code>
      </pre>
    </div>
  )
}
