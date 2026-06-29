import asyncio
import os
from typing import Optional

import httpx


def build_mentor_prompt(
    message: str,
    hint_level: str = "guided",
    challenge_context: Optional[str] = None,
    mode: str = "general",
    session_history: Optional[list[dict]] = None,
    session_summary: Optional[str] = None,
) -> str:
    """Create a mentor-style prompt that keeps the assistant tutoring instead of spoiling."""
    hint_level = (hint_level or "guided").strip().lower() or "guided"
    mode = (mode or "general").strip().lower() or "general"
    context_line = f"Challenge context: {challenge_context}" if challenge_context else "Challenge context: none provided"
    history_section = ""
    summary_section = ""

    if session_summary:
        summary_section = f"Session summary: {session_summary}\n"

    if session_history:
        history_lines = []
        for item in session_history[-10:]:
            role = item.get("role", "user")
            content = item.get("content", "")
            history_lines.append(f"{role}: {content}")
        history_section = "Session history:\n" + "\n".join(history_lines) + "\n"

    return (
        "You are Aide, a cybersecurity mentor. "
        "Teach progressively, do not give away the full solution, and guide the user with small steps. "
        f"Current hint level: {hint_level}. "
        f"Current mode: {mode}. "
        f"{context_line}. "
        + summary_section
        + history_section
        + "Prefer a helpful nudge, a focused explanation, and one next action. "
        + "If the user is stuck, ask a guiding question before giving a direct answer. "
        + f"User request: {message}"
    )


class LLMClient:
    """Provider-agnostic LLM client with simple OpenAI routing.

    Supported providers in Phase 2:
    - openai: uses OpenAI Chat Completions API with `api_key` and optional `model`.
    - generic: forwards to a provider `base_url` expecting a ChatCompletions-like endpoint.
    If `provider` is None or unsupported a helpful mentor-style stub message is returned.
    """

    def __init__(self):
        self.default_model = os.getenv("AIDE_DEFAULT_MODEL", "gpt-3.5-turbo")

    async def generate_reply(
        self,
        message: str,
        provider: Optional[dict] = None,
        hint_level: str = "guided",
        challenge_context: Optional[str] = None,
        mode: str = "general",
        session_history: Optional[list[dict]] = None,
        session_summary: Optional[str] = None,
    ) -> str:
        if provider and getattr(provider, "provider", None) is None:
            provider = dict(provider)

        mentor_prompt = build_mentor_prompt(
            message,
            hint_level=hint_level,
            challenge_context=challenge_context,
            mode=mode,
            session_history=session_history,
            session_summary=session_summary,
        )

        if provider and provider.get("provider") == "openai":
            return await self._openai_chat(mentor_prompt, provider)

        if provider and provider.get("provider") == "generic" and provider.get("base_url"):
            return await self._generic_chat(mentor_prompt, provider)

        await asyncio.sleep(0.01)
        return (
            "[Phase 2 mentor mode] I can guide you progressively. "
            f"Try this next step: {message}"
        )

    async def _openai_chat(self, message: str, provider: dict) -> str:
        api_key = provider.get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "OpenAI provider selected but no API key provided. Set `api_key` in provider config or OPENAI_API_KEY env var."

        model = provider.get("model") or self.default_model
        temperature = provider.get("temperature", 0.2)

        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            "temperature": temperature,
            "max_tokens": 800,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                # Defensive access
                choices = data.get("choices") or []
                if not choices:
                    return "OpenAI returned no choices."
                content = choices[0].get("message", {}).get("content") or choices[0].get("text")
                return content or "(empty response)"
            except httpx.HTTPError as e:
                return f"OpenAI request failed: {str(e)}"

    async def _generic_chat(self, message: str, provider: dict) -> str:
        base_url = provider.get("base_url")
        api_key = provider.get("api_key")
        model = provider.get("model") or self.default_model
        temperature = provider.get("temperature", 0.2)

        payload = {"model": model, "messages": [{"role": "user", "content": message}], "temperature": temperature}

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                resp = await client.post(base_url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                # Try to parse ChatCompletions-like reply
                choices = data.get("choices") or []
                if choices:
                    content = choices[0].get("message", {}).get("content") or choices[0].get("text")
                    return content or "(empty response)"
                # Fallback to top-level 'output' or 'result'
                for k in ("output", "result", "text"):
                    if k in data:
                        return data[k]
                return "Provider returned unexpected response shape."
            except httpx.HTTPError as e:
                return f"Provider request failed: {str(e)}"
