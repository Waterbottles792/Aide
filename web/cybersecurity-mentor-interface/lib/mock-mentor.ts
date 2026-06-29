import type { HintLevel, Mode } from './types'

// Placeholder mentor response. This is intentionally isolated so it can be
// replaced by a real streaming backend / RAG call without touching the UI.
export function buildMentorReply(
  prompt: string,
  mode: Mode,
  hintLevel: HintLevel,
): string {
  const topic = prompt.length > 60 ? `${prompt.slice(0, 57)}…` : prompt

  return `Great question about **${topic}**. Let's reason through it together rather than jumping to the answer.

Here's how I'd approach this in **${mode}** mode at a **${hintLevel}** hint level:

1. **Clarify the goal** — what exactly are we trying to achieve or access?
2. **Enumerate** — gather everything observable before acting.
3. **Form a hypothesis** — what weakness might exist, and why?

A quick example of structured recon:

\`\`\`bash
# Map the attack surface first
nmap -sC -sV -oN scan.txt target.local
\`\`\`

| Step | Why it matters |
| --- | --- |
| Recon | Reveals the real surface |
| Hypothesis | Keeps you focused |
| Validation | Confirms before exploiting |

> Tip: I won't hand you flags directly — I'll guide your reasoning so the skill sticks.

What have you observed so far? Share your findings and I'll point you toward the next step.`
}
