import type {
  HintLevelOption,
  ModeOption,
  ProviderStatus,
  Session,
} from './types'

// These collections stand in for backend-provided config. The UI never
// hardcodes them inline so they can be swapped for API data later.

export const MODE_OPTIONS: ModeOption[] = [
  {
    value: 'general',
    label: 'General',
    description: 'Broad security guidance and study help',
  },
  {
    value: 'web',
    label: 'Web Security',
    description: 'OWASP, injection, auth, and app logic flaws',
  },
  {
    value: 'network',
    label: 'Network Security',
    description: 'Recon, services, pivoting, and protocols',
  },
  {
    value: 'ctf',
    label: 'CTF',
    description: 'Capture-the-flag reasoning and methodology',
  },
  {
    value: 'bugbounty',
    label: 'Bug Bounty',
    description: 'Scope, triage, and responsible disclosure',
  },
  {
    value: 'scripting',
    label: 'Scripting',
    description: 'Python, Bash, and tooling automation',
  },
]

export const HINT_LEVEL_OPTIONS: HintLevelOption[] = [
  {
    value: 'guided',
    label: 'Guided',
    description: 'Step-by-step nudges, no spoilers',
  },
  {
    value: 'beginner',
    label: 'Beginner',
    description: 'Plenty of context and definitions',
  },
  {
    value: 'intermediate',
    label: 'Intermediate',
    description: 'Assumes core fundamentals',
  },
  {
    value: 'advanced',
    label: 'Advanced',
    description: 'Terse, expert-level reasoning',
  },
]

export const DEFAULT_PROVIDER: ProviderStatus = {
  provider: 'Aide Gateway',
  model: 'aide-sec-pro',
  ready: true,
}

export const INITIAL_SESSIONS: Session[] = [
  {
    id: 'sess-1',
    title: 'SQLi on login portal',
    mode: 'web',
    updatedAt: Date.now() - 1000 * 60 * 24,
  },
  {
    id: 'sess-2',
    title: 'Nmap service enumeration',
    mode: 'network',
    updatedAt: Date.now() - 1000 * 60 * 60 * 3,
  },
  {
    id: 'sess-3',
    title: 'Reverse shell stabilization',
    mode: 'scripting',
    updatedAt: Date.now() - 1000 * 60 * 60 * 26,
  },
  {
    id: 'sess-4',
    title: 'JWT none-alg bypass',
    mode: 'bugbounty',
    updatedAt: Date.now() - 1000 * 60 * 60 * 50,
  },
]

export function formatRelativeTime(timestamp: number): string {
  const diff = Date.now() - timestamp
  const minutes = Math.round(diff / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes}m ago`
  const hours = Math.round(minutes / 60)
  if (hours < 24) return `${hours}h ago`
  const days = Math.round(hours / 24)
  return `${days}d ago`
}
