// Domain types for Aide. Kept backend-agnostic so these can later be hydrated
// from an API / RAG layer without touching the UI components.

export type Role = 'user' | 'assistant'

export type Mode = 'general' | 'web' | 'network' | 'ctf' | 'bugbounty' | 'scripting'

export type HintLevel = 'guided' | 'beginner' | 'intermediate' | 'advanced'

export interface Message {
  id: string
  role: Role
  content: string
  createdAt: number
}

export interface Session {
  id: string
  title: string
  mode: Mode
  updatedAt: number
}

export interface ProviderStatus {
  provider: string
  model: string
  ready: boolean
}

export interface ModeOption {
  value: Mode
  label: string
  description: string
}

export interface HintLevelOption {
  value: HintLevel
  label: string
  description: string
}
