import {
  BroadcastIcon,
  BugIcon,
  CodeIcon,
  GlobeIcon,
  ShieldCheckIcon,
  TerminalIcon,
} from '@primer/octicons-react'
import type { Mode } from '@/lib/types'

// Single source of truth for the icon that represents each learning mode.
const MODE_ICONS: Record<Mode, React.ComponentType<{ size?: number }>> = {
  general: ShieldCheckIcon,
  web: GlobeIcon,
  network: BroadcastIcon,
  ctf: TerminalIcon,
  bugbounty: BugIcon,
  scripting: CodeIcon,
}

export function getModeIcon(mode: Mode) {
  return MODE_ICONS[mode]
}

export function ModeIcon({ mode, size = 16 }: { mode: Mode; size?: number }) {
  const Icon = MODE_ICONS[mode]
  return <Icon size={size} />
}
