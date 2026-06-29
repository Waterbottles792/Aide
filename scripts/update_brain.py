from pathlib import Path
from datetime import datetime

root = Path(__file__).resolve().parents[1]
brain = root / 'brain.md'

summary = f"""# Aide — Brain

## Project identity
Aide is a desktop-first GenAI mentor for cybersecurity learning platforms such as TryHackMe, HackTheBox, PortSwigger, and CTFs. It is designed to teach progressively rather than spoil solutions.

## Current state
- Phase 1 is implemented: FastAPI backend with `/health` and `/chat`, provider-aware LLM routing, a simple React/Vite frontend, and provider settings storage.
- Provider storage is implemented with OS keyring first and an encrypted-file fallback for headless or non-keyring environments.
- The repo is now organized around the `aide` package path under `Rufus/aide`.
- Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Architecture
- Backend: FastAPI in `Rufus/aide/app/backend`
- Frontend: React/Vite in `Rufus/aide/app/frontend/react-app`
- Core modules:
  - `main.py`: API entrypoint
  - `llm_client.py`: provider-agnostic LLM call wrapper
  - `provider_store.py`: secrets + provider-config persistence

## Current priorities
1. Keep Phase 1 usable end to end: backend + frontend + provider config.
2. Add richer hinting and context handling in later phases.
3. Preserve this file as a compact living summary for future sessions.

## Operational notes
- Backend run command: `python -m uvicorn aide.app.backend.main:app --reload --port 8000`
- Frontend run command: `npm run dev` inside `Rufus/aide/app/frontend/react-app`
- Secrets are stored in the OS keyring when possible, and in encrypted local files when not.

## Update policy
Whenever significant implementation work happens, update this file with the latest architecture, state, and next priorities so a new session can recover context quickly.
"""

brain.write_text(summary)
print(f'updated {brain}')
