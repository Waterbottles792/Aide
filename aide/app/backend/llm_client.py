import asyncio
import os
from typing import Optional

import httpx


class LLMClient:
    """Provider-agnostic LLM client with simple OpenAI routing.

    Supported providers in Phase 1:
    - openai: uses OpenAI Chat Completions API with `api_key` and optional `model`.
    - generic: forwards to a provider `base_url` expecting a ChatCompletions-like endpoint.
    If `provider` is None or unsupported a helpful stub message is returned.
    """

    def __init__(self):
        self.default_model = os.getenv("AIDE_DEFAULT_MODEL", "gpt-3.5-turbo")

    async def generate_reply(self, message: str, provider: Optional[dict] = None) -> str:
        if provider and getattr(provider, "provider", None) is None:
            # allow dict-like access
            provider = dict(provider)

        if provider and provider.get("provider") == "openai":
            return await self._openai_chat(message, provider)

        if provider and provider.get("provider") == "generic" and provider.get("base_url"):
            return await self._generic_chat(message, provider)

        # Fallback stub
        await asyncio.sleep(0.01)
        return f"[Phase 1 stub] I received your message: {message}\n(Configure a provider to get real LLM replies.)"

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
