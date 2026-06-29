'use client'

import type { CSSProperties, ReactNode } from 'react'

interface GlassCardProps {
  children: ReactNode
  /** Adds a hover lift + accent glow. */
  interactive?: boolean
  raised?: boolean
  style?: CSSProperties
  className?: string
  as?: 'div' | 'section' | 'article'
}

/**
 * Token-styled glass surface. Primer's general Card is image-shaped, so per the
 * patterns guidance we use a bordered token-styled container for generic
 * surfaces. Colors/radii/shadows all come from primitives.
 */
export function GlassCard({
  children,
  interactive = false,
  raised = false,
  style,
  className,
  as: Tag = 'div',
}: GlassCardProps) {
  return (
    <Tag
      className={[
        raised ? 'aide-glass-raised' : 'aide-glass',
        interactive ? 'aide-glow-hover' : '',
        className ?? '',
      ]
        .filter(Boolean)
        .join(' ')}
      style={{
        borderRadius: 'var(--borderRadius-large)',
        boxShadow: 'var(--shadow-resting-medium)',
        ...style,
      }}
    >
      {children}
    </Tag>
  )
}
