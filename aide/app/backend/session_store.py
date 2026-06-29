import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


class SessionStore:
    """Persist user sessions and session summaries for Aide."""

    STORAGE_FILENAME = "sessions.json"

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = Path(storage_dir) if storage_dir else Path(__file__).parent
        self.file = self.storage_dir / self.STORAGE_FILENAME
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not self.file.exists():
            self._write_sessions({})

    def _read_sessions(self) -> dict:
        try:
            return json.loads(self.file.read_text())
        except Exception:
            return {}

    def _write_sessions(self, data: dict) -> None:
        self.file.write_text(json.dumps(data, indent=2))

    def _now_iso(self) -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    def create_session(
        self,
        name: str = "Untitled session",
        summary: str = "",
        hint_level: str = "guided",
        challenge_context: Optional[str] = None,
        mode: str = "general",
        history: Optional[list[dict]] = None,
    ) -> dict:
        sessions = self._read_sessions()
        session_id = uuid.uuid4().hex
        obj = {
            "session_id": session_id,
            "name": name,
            "summary": summary or "",
            "hint_level": hint_level or "guided",
            "challenge_context": challenge_context or "",
            "mode": mode or "general",
            "history": history or [],
            "created_at": self._now_iso(),
            "updated_at": self._now_iso(),
        }
        sessions[session_id] = obj
        self._write_sessions(sessions)
        return obj

    def get_session(self, session_id: str) -> dict | None:
        return self._read_sessions().get(session_id)

    def list_sessions(self) -> list[dict]:
        return [
            {
                "session_id": sid,
                "name": session.get("name", "Untitled session"),
                "summary": session.get("summary", ""),
                "hint_level": session.get("hint_level", "guided"),
                "challenge_context": session.get("challenge_context", ""),
                "mode": session.get("mode", "general"),
                "turns": len(session.get("history", [])),
                "created_at": session.get("created_at"),
                "updated_at": session.get("updated_at"),
            }
            for sid, session in self._read_sessions().items()
        ]

    def save_session(self, session: dict) -> dict:
        sessions = self._read_sessions()
        session["updated_at"] = self._now_iso()
        sessions[session["session_id"]] = session
        self._write_sessions(sessions)
        return session

    def delete_session(self, session_id: str) -> bool:
        sessions = self._read_sessions()
        if session_id in sessions:
            sessions.pop(session_id)
            self._write_sessions(sessions)
            return True
        return False
